import os
import uuid
import math
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Report, User, ReportLike, Comment, Notification
from app.schemas import ReportResponse, ReportCreate, ReportStatusUpdate, CommentResponse, CommentCreate
from app.auth import get_current_user, get_current_admin
from app.services.municipality_client import dispatch_report_to_municipality
from sqlalchemy.orm import joinedload, selectinload
from app.services.cache import cache_service

router = APIRouter(prefix="/api/reports", tags=["Reportes"])

ERROR_REPORT_NOT_FOUND = "Reporte no encontrado"

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")

def invalidate_all_reports_cache():
    cache_service.invalidate_prefix("reports:")
    cache_service.invalidate_prefix("users:reports:")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Haversine formula
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no soportado. Use imágenes JPG, PNG, WEBP o GIF."
        )
        
    filename = f"{uuid.uuid4().hex}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar la imagen: {str(exc)}"
        )
        
    return {"url": f"/static/uploads/{filename}"}

@router.get("", response_model=List[ReportResponse])
def get_reports(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    search: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Cache lookup
    cache_key = f"reports:user_{current_user.id}:cat_{category}:sev_{severity}:q_{search}:lat_{lat}:lng_{lng}:r_{radius_km}:skip_{skip}:limit_{limit}"
    cached_data = cache_service.get(cache_key)
    if cached_data is not None:
        return cached_data

    # Eager load relationships to prevent N+1 queries
    query = db.query(Report).options(
        joinedload(Report.author),
        selectinload(Report.likes),
        selectinload(Report.comments)
    )
    
    if category:
        query = query.filter(Report.category == category)
        
    if severity:
        query = query.filter(Report.severity == severity)
        
    if search:
        query = query.filter(
            Report.title.ilike(f"%{search}%") | Report.description.ilike(f"%{search}%")
        )
        
    reports = query.order_by(Report.created_at.desc()).all()
    
    # Filter by radius if parameters are supplied
    if lat is not None and lng is not None and radius_km is not None:
        filtered_reports = []
        for report in reports:
            dist = calculate_distance_km(lat, lng, report.latitude, report.longitude)
            if dist <= radius_km:
                filtered_reports.append(report)
        reports = filtered_reports
        
    # Apply pagination skip/limit
    reports = reports[skip : skip + limit]
        
    # Build schema models
    results = []
    for report in reports:
        likes_count = len(report.likes)
        comments_count = len(report.comments)
        user_liked = any(like.user_id == current_user.id for like in report.likes)
        
        results.append(ReportResponse(
            id=report.id,
            title=report.title,
            description=report.description,
            latitude=report.latitude,
            longitude=report.longitude,
            address=report.address,
            category=report.category,
            severity=report.severity,
            status=report.status,
            municipality_ticket=report.municipality_ticket,
            image_urls=report.image_urls,
            created_at=report.created_at,
            author=report.author,
            likes_count=likes_count,
            comments_count=comments_count,
            user_liked=user_liked
        ))
        
    cache_service.set(cache_key, results)
    return results

@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_report = Report(
        title=report_data.title,
        description=report_data.description,
        latitude=report_data.latitude,
        longitude=report_data.longitude,
        address=report_data.address,
        category=report_data.category,
        severity=report_data.severity,
        image_urls=report_data.image_urls,
        author_id=current_user.id
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    invalidate_all_reports_cache()
    
    # If the report is critical, auto-dispatch to the municipality API
    if new_report.severity.lower() in ["critical", "critico"]:
        ticket = await dispatch_report_to_municipality(
            report_id=new_report.id,
            title=new_report.title,
            description=new_report.description,
            category=new_report.category,
            latitude=new_report.latitude,
            longitude=new_report.longitude,
            address=new_report.address or "",
            severity=new_report.severity,
            reporter_name=current_user.full_name,
            reporter_email=current_user.email
        )
        new_report.status = "derivado_muni"
        new_report.municipality_ticket = ticket
        db.commit()
        db.refresh(new_report)
        
        # Create a notification for the creator
        notification = Notification(
            user_id=current_user.id,
            title="Incidencia Derivada de Inmediato",
            body=f"Tu reporte crítico '{new_report.title}' fue despachado a la municipalidad. Folio: {ticket}",
            type="municipal_dispatch",
            related_report_id=new_report.id
        )
        db.add(notification)

        # Notify other users within their configured notification radius
        other_users = db.query(User).filter(
            User.id != current_user.id,
            User.notifications_enabled == True
        ).all()
        
        for u in other_users:
            dist = calculate_distance_km(u.latitude, u.longitude, new_report.latitude, new_report.longitude)
            if dist <= u.notification_radius_km:
                nearby_notification = Notification(
                    user_id=u.id,
                    title="¡Alerta Crítica en tu zona!",
                    body=f"Se ha reportado un incidente crítico '{new_report.title}' a {dist:.1f} km de tu ubicación.",
                    type="critical_alert",
                    related_report_id=new_report.id
                )
                db.add(nearby_notification)
        db.commit()

    # Calculate statistics
    return ReportResponse(
        id=new_report.id,
        title=new_report.title,
        description=new_report.description,
        latitude=new_report.latitude,
        longitude=new_report.longitude,
        address=new_report.address,
        category=new_report.category,
        severity=new_report.severity,
        status=new_report.status,
        municipality_ticket=new_report.municipality_ticket,
        image_urls=new_report.image_urls,
        created_at=new_report.created_at,
        author=new_report.author,
        likes_count=0,
        comments_count=0,
        user_liked=False
    )

@router.get("/{report_id}", response_model=ReportResponse)
def get_report_detail(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).options(
        joinedload(Report.author),
        selectinload(Report.likes),
        selectinload(Report.comments)
    ).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_REPORT_NOT_FOUND
        )
        
    likes_count = len(report.likes)
    comments_count = len(report.comments)
    user_liked = any(like.user_id == current_user.id for like in report.likes)
    
    return ReportResponse(
        id=report.id,
        title=report.title,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        address=report.address,
        category=report.category,
        severity=report.severity,
        status=report.status,
        municipality_ticket=report.municipality_ticket,
        image_urls=report.image_urls,
        created_at=report.created_at,
        author=report.author,
        likes_count=likes_count,
        comments_count=comments_count,
        user_liked=user_liked
    )

@router.post("/{report_id}/like")
def toggle_like_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_REPORT_NOT_FOUND
        )
        
    like = db.query(ReportLike).filter(
        ReportLike.report_id == report_id,
        ReportLike.user_id == current_user.id
    ).first()
    
    if like:
        db.delete(like)
        db.commit()
        invalidate_all_reports_cache()
        return {"liked": False, "message": "Reacción eliminada exitosamente"}
    else:
        new_like = ReportLike(report_id=report_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        
        # Notify report owner if someone else likes
        if report.author_id != current_user.id:
            notification = Notification(
                user_id=report.author_id,
                title="Nueva reacción en tu reporte",
                body=f"A {current_user.full_name} le gusta tu reporte '{report.title}'",
                type="new_like",
                related_report_id=report.id
            )
            db.add(notification)
            db.commit()
            
        invalidate_all_reports_cache()
        return {"liked": True, "message": "Reacción agregada exitosamente"}

@router.get("/{report_id}/comments", response_model=List[CommentResponse])
def get_comments(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_REPORT_NOT_FOUND
        )
    comments = db.query(Comment).options(
        joinedload(Comment.author)
    ).filter(Comment.report_id == report_id).order_by(Comment.created_at.asc()).all()
    return comments

@router.post("/{report_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    report_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_REPORT_NOT_FOUND
        )
        
    new_comment = Comment(
        report_id=report_id,
        author_id=current_user.id,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    invalidate_all_reports_cache()
    
    # Notify report owner if someone else comments
    if report.author_id != current_user.id:
        notification = Notification(
            user_id=report.author_id,
            title="Nuevo comentario en tu reporte",
            body=f"{current_user.full_name} comentó: '{comment_data.content[:40]}...'",
            type="new_comment",
            related_report_id=report.id
        )
        db.add(notification)
        db.commit()
        
    return new_comment

# ----------------- ADMIN ENDPOINTS -----------------

@router.get("/admin/all-reports", response_model=List[ReportResponse])
def get_all_reports_for_admin(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Admin console wants to list all reports with no proximity restrictions
    reports = db.query(Report).options(
        joinedload(Report.author),
        selectinload(Report.likes),
        selectinload(Report.comments)
    ).order_by(Report.created_at.desc()).all()
    
    results = []
    for report in reports:
        likes_count = len(report.likes)
        comments_count = len(report.comments)
        user_liked = any(like.user_id == current_user.id for like in report.likes)
        
        results.append(ReportResponse(
            id=report.id,
            title=report.title,
            description=report.description,
            latitude=report.latitude,
            longitude=report.longitude,
            address=report.address,
            category=report.category,
            severity=report.severity,
            status=report.status,
            municipality_ticket=report.municipality_ticket,
            image_urls=report.image_urls,
            created_at=report.created_at,
            author=report.author,
            likes_count=likes_count,
            comments_count=comments_count,
            user_liked=user_liked
        ))
    return results

def _validate_status_transition(current_user: User, report: Report, new_status: str) -> None:
    # Check authorization: user must be admin OR the author of the report
    if current_user.role != "admin" and report.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar el estado de este reporte."
        )
    allowed_statuses = ["abierto", "derivado_muni", "resuelto", "rechazado"]
    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estado inválido. Los estados permitidos son: abierto, derivado_muni, resuelto, rechazado."
        )
    # Citizens can only change status to "resuelto" or "abierto"
    if current_user.role != "admin" and new_status not in ["abierto", "resuelto"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los ciudadanos solo pueden cambiar el estado a 'resuelto' o 'abierto'."
        )


def _notify_status_update(db: Session, report: Report, current_user: User, old_status: str, new_status: str) -> None:
    # Create notification for report author (only if changed by another user, i.e., admin)
    if report.author_id != current_user.id:
        notification = Notification(
            user_id=report.author_id,
            title="Actualización de estado en tu reporte",
            body=f"El estado del reporte '{report.title}' cambió de '{old_status}' a '{new_status}'.",
            type="report_status",
            related_report_id=report.id
        )
        db.add(notification)
        db.commit()
        
    # Notify other users in the area when a report is resolved
    if new_status == "resuelto" and old_status != "resuelto":
        other_users = db.query(User).filter(
            User.id != report.author_id,
            User.notifications_enabled == True
        ).all()
        for u in other_users:
            dist = calculate_distance_km(u.latitude, u.longitude, report.latitude, report.longitude)
            if dist <= u.notification_radius_km:
                resolved_notification = Notification(
                    user_id=u.id,
                    title="¡Problema resuelto en tu zona!",
                    body=f"El reporte de '{report.title}' a {dist:.1f} km de tu ubicación ha sido marcado como Resuelto.",
                    type="report_resolved",
                    related_report_id=report.id
                )
                db.add(resolved_notification)
        db.commit()


@router.put("/{report_id}/status", response_model=ReportResponse)
async def update_report_status(
    report_id: int,
    status_update: ReportStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).options(
        joinedload(Report.author),
        selectinload(Report.likes),
        selectinload(Report.comments)
    ).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_REPORT_NOT_FOUND
        )
        
    old_status = report.status
    new_status = status_update.status.lower()
    _validate_status_transition(current_user, report, new_status)
    report.status = new_status
    
    # If state changes to derivado_muni and ticket is empty, trigger simulation dispatch
    if new_status == "derivado_muni" and not report.municipality_ticket:
        reporter = db.query(User).filter(User.id == report.author_id).first()
        ticket = await dispatch_report_to_municipality(
            report_id=report.id,
            title=report.title,
            description=report.description,
            category=report.category,
            latitude=report.latitude,
            longitude=report.longitude,
            address=report.address or "",
            severity=report.severity,
            reporter_name=reporter.full_name if reporter else "Ciudadano ComuniSafe",
            reporter_email=reporter.email if reporter else "info@comunisafe.cl"
        )
        report.municipality_ticket = ticket
        
    db.commit()
    db.refresh(report)
    _notify_status_update(db, report, current_user, old_status, new_status)
    invalidate_all_reports_cache()
    
    likes_count = len(report.likes)
    comments_count = len(report.comments)
    user_liked = any(like.user_id == current_user.id for like in report.likes)
    
    return ReportResponse(
        id=report.id,
        title=report.title,
        description=report.description,
        latitude=report.latitude,
        longitude=report.longitude,
        address=report.address,
        category=report.category,
        severity=report.severity,
        status=report.status,
        municipality_ticket=report.municipality_ticket,
        image_urls=report.image_urls,
        created_at=report.created_at,
        author=report.author,
        likes_count=likes_count,
        comments_count=comments_count,
        user_liked=user_liked
    )
