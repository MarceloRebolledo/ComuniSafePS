import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base, SessionLocal
from app.routers import auth, users, reports, notifications
from app.models import User, Report, Comment
from app.auth import get_password_hash

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

DEFAULT_MOCK_LOCATION = "Temuco, Chile"

def seed_mock_data():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            # Add mock users
            citizen = User(
                email="citizen@comunisafe.cl",
                password_hash=get_password_hash("password123"),
                full_name="María García",
                role="citizen",
                bio="Vecina activa comprometida con mejorar nuestra comunidad en Temuco.",
                location=DEFAULT_MOCK_LOCATION,
                latitude=-38.735,
                longitude=-72.590,
                notifications_enabled=True,
                notification_radius_km=5.0,
                is_verified=True
            )
            carlos = User(
                email="carlos@comunisafe.cl",
                password_hash=get_password_hash("password123"),
                full_name="Carlos Rodríguez",
                role="citizen",
                bio="Comprometido con el medio ambiente y el desarrollo comunitario local.",
                location=DEFAULT_MOCK_LOCATION,
                latitude=-38.739,
                longitude=-72.592,
                notifications_enabled=True,
                notification_radius_km=10.0,
                is_verified=True
            )
            admin = User(
                email="admin@comunisafe.cl",
                password_hash=get_password_hash("adminpassword"),
                full_name="Administrador Municipal",
                role="admin",
                bio="Cuenta oficial de soporte y administración para ComuniSafe.",
                location=DEFAULT_MOCK_LOCATION,
                latitude=-38.737,
                longitude=-72.591,
                notifications_enabled=True,
                notification_radius_km=15.0,
                is_verified=True
            )
            db.add_all([citizen, carlos, admin])
            db.commit()
            
            # Add mock reports
            r1 = Report(
                title="Bache en Av. Alemania",
                description="Hoyo grande en la avenida que complica el tránsito vehicular. Lleva más de dos semanas y representa un riesgo real para autos, motos y ciclistas.",
                latitude=-38.731,
                longitude=-72.598,
                address="Av. Alemania 0290, Temuco",
                category="Calles",
                severity="normal",
                status="abierto",
                image_urls=["https://images.unsplash.com/photo-1539034629914-0e70a1243587?auto=format&fit=crop&w=1080&q=80"],
                author_id=citizen.id
            )
            r2 = Report(
                title="Microbasural creciendo",
                description="Acumulación de basura cerca de la plaza que ya afecta a todo el sector. Los vecinos llevamos semanas pidiendo limpieza en este punto.",
                latitude=-38.737,
                longitude=-72.591,
                address="Plaza Aníbal Pinto, Temuco",
                category="Basura",
                severity="normal",
                status="abierto",
                image_urls=["https://images.unsplash.com/photo-1762805544291-cb128cf5ec80?auto=format&fit=crop&w=1080&q=80"],
                author_id=carlos.id
            )
            r3 = Report(
                title="Incendio visible en Cerro Ñielol",
                description="Humo negro y llamas visibles avanzando rápidamente por la ladera norte del cerro. Bomberos ya han sido alertados y se recomienda no acercarse al lugar.",
                latitude=-38.722,
                longitude=-72.587,
                address="Cerro Ñielol sector norte, Temuco",
                category="Seguridad",
                severity="critico",
                status="derivado_muni",
                municipality_ticket="MUNI-TICKET-92837",
                image_urls=["https://images.unsplash.com/photo-1767416129512-2012f3156f5b?auto=format&fit=crop&w=1080&q=80"],
                author_id=carlos.id
            )
            db.add_all([r1, r2, r3])
            db.commit()
            
            # Comments
            c1 = Comment(
                report_id=r1.id,
                author_id=carlos.id,
                content="Ya llevo una semana pasando por ahí con cuidado. Ojalá lo arreglen pronto."
            )
            c2 = Comment(
                report_id=r3.id,
                author_id=citizen.id,
                content="Yo también lo veo desde mi casa. El humo es muy oscuro y denso."
            )
            db.add_all([c1, c2])
            db.commit()
    finally:
        db.close()

import sys
if "pytest" not in sys.modules:
    seed_mock_data()

app = FastAPI(
    title="ComuniSafe API",
    description="API de backend para ComuniSafe, construida en FastAPI con soporte de SQLite, roles de usuario y simulación de derivación municipal.",
    version="1.0.0"
)

# CORS configuration to allow local web/mobile clients to access endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static/uploads directories exist and mount StaticFiles
static_dir = os.path.join(os.path.dirname(__file__), "static")
uploads_dir = os.path.join(static_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(reports.router)
app.include_router(notifications.router)

@app.get("/")
def read_root():
    return {
        "app": "ComuniSafe Backend",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs"
    }

