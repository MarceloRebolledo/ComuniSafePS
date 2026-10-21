import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db
from app.config import settings
from app.models import User

# Setup isolated in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency in app
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True, scope="function")
def run_around_tests():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

def verify_user(email: str):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
    db.close()

def test_email_verification():
    # Register
    register_response = client.post(
        "/api/auth/register",
        json={"email": "testverify@comunisafe.cl", "password": "password123", "full_name": "Test Verify"}
    )
    assert register_response.status_code == 201
    
    # Get code from DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "testverify@comunisafe.cl").first()
    code = user.verification_code
    assert code is not None
    db.close()
    
    # Try login (should fail with 403)
    login_fail = client.post(
        "/api/auth/login",
        data={"username": "testverify@comunisafe.cl", "password": "password123"}
    )
    assert login_fail.status_code == 403
    
    # Verify email
    verify_resp = client.post(
        "/api/auth/verify-email",
        json={"email": "testverify@comunisafe.cl", "code": code}
    )
    assert verify_resp.status_code == 200
    
    # Try login again (should succeed)
    login_ok = client.post(
        "/api/auth/login",
        data={"username": "testverify@comunisafe.cl", "password": "password123"}
    )
    assert login_ok.status_code == 200

def test_user_registration_and_login():
    # Register citizen
    register_response = client.post(
        "/api/auth/register",
        json={"email": "citizen@comunisafe.cl", "password": "password123", "full_name": "Juan Perez"}
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "citizen@comunisafe.cl"
    assert register_response.json()["role"] == "citizen"

    # Verify user
    verify_user("citizen@comunisafe.cl")

    # Login
    login_response = client.post(
        "/api/auth/login",
        data={"username": "citizen@comunisafe.cl", "password": "password123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    token = login_response.json()["access_token"]

    # Profile
    profile_response = client.get(
        "/api/users/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["full_name"] == "Juan Perez"

def test_report_creation_and_municipality_dispatch():
    # 1. Register a second citizen (Carlos) to test nearby notification
    client.post(
        "/api/auth/register",
        json={"email": "carlos@comunisafe.cl", "password": "password123", "full_name": "Carlos Rodriguez"}
    )
    verify_user("carlos@comunisafe.cl")
    
    carlos_token = client.post(
        "/api/auth/login",
        data={"username": "carlos@comunisafe.cl", "password": "password123"}
    ).json()["access_token"]
    
    # Carlos updates their profile to Santiago coords (close to the critical report)
    client.put(
        "/api/users/profile",
        json={
            "latitude": -33.457,
            "longitude": -70.649,
            "notification_radius_km": 5.0,
            "notifications_enabled": True
        },
        headers={"Authorization": f"Bearer {carlos_token}"}
    )

    # Register and login citizen (Juan)
    client.post(
        "/api/auth/register",
        json={"email": "citizen@comunisafe.cl", "password": "password123", "full_name": "Juan Perez"}
    )
    verify_user("citizen@comunisafe.cl")
    
    token = client.post(
        "/api/auth/login",
        data={"username": "citizen@comunisafe.cl", "password": "password123"}
    ).json()["access_token"]

    # 1. Create a medium report (regular flow)
    report_response = client.post(
        "/api/reports",
        json={
            "title": "Bache en Avenida",
            "description": "Hoyos considerables en el pavimento",
            "latitude": -33.456,
            "longitude": -70.648,
            "address": "Av. Vitacura 1230",
            "category": "pothole",
            "severity": "medium",
            "image_urls": ["/static/uploads/bache.jpg"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert report_response.status_code == 201
    report_data = report_response.json()
    assert report_data["status"] == "abierto"
    assert report_data["municipality_ticket"] is None

    # 2. Create a critical report (triggers automatic dispatch & nearby notification)
    critical_response = client.post(
        "/api/reports",
        json={
            "title": "Semáforo apagado en intersección",
            "description": "Gran congestión y riesgo de colisiones",
            "latitude": -33.457,
            "longitude": -70.649,
            "address": "Av. Providencia con Pedro de Valdivia",
            "category": "lighting",
            "severity": "critical",
            "image_urls": ["/static/uploads/semaforo.jpg"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert critical_response.status_code == 201
    critical_data = critical_response.json()
    assert critical_data["status"] == "derivado_muni"
    assert critical_data["municipality_ticket"] is not None
    assert "MUNI-TICKET-" in critical_data["municipality_ticket"]

    # Check creator (Juan) notification was created
    notifications_resp = client.get(
        "/api/notifications",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert notifications_resp.status_code == 200
    notifications = notifications_resp.json()
    assert len(notifications) == 1
    assert "Incidencia Derivada de Inmediato" in notifications[0]["title"]

    # Check Carlos (nearby user) received the nearby critical notification!
    carlos_notifications_resp = client.get(
        "/api/notifications",
        headers={"Authorization": f"Bearer {carlos_token}"}
    )
    assert carlos_notifications_resp.status_code == 200
    carlos_notifications = carlos_notifications_resp.json()
    assert len(carlos_notifications) == 1
    assert "¡Alerta Crítica en tu zona!" in carlos_notifications[0]["title"]
    assert "Semáforo apagado" in carlos_notifications[0]["body"]

def test_report_interaction_likes_comments():
    # Register and login citizen
    client.post(
        "/api/auth/register",
        json={"email": "citizen@comunisafe.cl", "password": "password123", "full_name": "Juan Perez"}
    )
    verify_user("citizen@comunisafe.cl")
    
    token = client.post(
        "/api/auth/login",
        data={"username": "citizen@comunisafe.cl", "password": "password123"}
    ).json()["access_token"]

    # Create report
    report_response = client.post(
        "/api/reports",
        json={
            "title": "Bache en Avenida",
            "description": "Hoyos en pavimento",
            "latitude": -33.456,
            "longitude": -70.648,
            "category": "pothole",
            "severity": "medium",
            "image_urls": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    report_id = report_response.json()["id"]

    # Toggle like (Like)
    like_response = client.post(
        f"/api/reports/{report_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert like_response.status_code == 200
    assert like_response.json()["liked"] is True

    # Check report state
    get_report = client.get(
        f"/api/reports/{report_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_report.json()["likes_count"] == 1
    assert get_report.json()["user_liked"] is True

    # Toggle like (Unlike)
    unlike_response = client.post(
        f"/api/reports/{report_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert unlike_response.status_code == 200
    assert unlike_response.json()["liked"] is False

    # Post Comment
    comment_response = client.post(
        f"/api/reports/{report_id}/comments",
        json={"content": "Yo también vi esto hoy en la mañana."},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert comment_response.status_code == 201
    assert comment_response.json()["content"] == "Yo también vi esto hoy en la mañana."

    # List Comments
    comments_response = client.get(
        f"/api/reports/{report_id}/comments",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert len(comments_response.json()) == 1

def test_admin_workflows():
    # 1. Register and login citizen
    client.post(
        "/api/auth/register",
        json={"email": "citizen@comunisafe.cl", "password": "password123", "full_name": "Juan Perez"}
    )
    verify_user("citizen@comunisafe.cl")
    
    citizen_token = client.post(
        "/api/auth/login",
        data={"username": "citizen@comunisafe.cl", "password": "password123"}
    ).json()["access_token"]

    # Create report
    report_response = client.post(
        "/api/reports",
        json={
            "title": "Poste inclinado",
            "description": "Poste de luz a punto de caer",
            "latitude": -33.456,
            "longitude": -70.648,
            "category": "lighting",
            "severity": "high",
            "image_urls": []
        },
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    report_id = report_response.json()["id"]

    # 2. Register and login admin (email starts with 'admin' to grant role)
    client.post(
        "/api/auth/register",
        json={"email": "admin@comunisafe.cl", "password": "adminpassword", "full_name": "Administrador Municipal"}
    )
    verify_user("admin@comunisafe.cl")
    
    admin_token = client.post(
        "/api/auth/login",
        data={"username": "admin@comunisafe.cl", "password": "adminpassword"}
    ).json()["access_token"]

    # 3. Regular citizen tries to update status (should fail with 403)
    status_fail = client.put(
        f"/api/reports/{report_id}/status",
        json={"status": "derivado_muni"},
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    assert status_fail.status_code == 403

    # 4. Admin updates status to derivado_muni (should succeed and generate ticket)
    status_ok = client.put(
        f"/api/reports/{report_id}/status",
        json={"status": "derivado_muni"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert status_ok.status_code == 200
    assert status_ok.json()["status"] == "derivado_muni"
    assert status_ok.json()["municipality_ticket"] is not None
    assert "MUNI-TICKET-" in status_ok.json()["municipality_ticket"]

    # 5. Check citizen received a notification about the status change
    notifications_resp = client.get(
        "/api/notifications",
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    assert len(notifications_resp.json()) == 1
    assert "Actualización de estado en tu reporte" in notifications_resp.json()[0]["title"]

    # 6. Author citizen updates status to resolved (should succeed)
    status_resolved = client.put(
        f"/api/reports/{report_id}/status",
        json={"status": "resuelto"},
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    assert status_resolved.status_code == 200
    assert status_resolved.json()["status"] == "resuelto"

    # 7. Register a second citizen who is not the author
    client.post(
        "/api/auth/register",
        json={"email": "citizen2@comunisafe.cl", "password": "password123", "full_name": "Vecino Dos"}
    )
    verify_user("citizen2@comunisafe.cl")
    citizen2_token = client.post(
        "/api/auth/login",
        data={"username": "citizen2@comunisafe.cl", "password": "password123"}
    ).json()["access_token"]

    # 8. Second citizen tries to modify status (should fail with 403)
    status_unauth = client.put(
        f"/api/reports/{report_id}/status",
        json={"status": "abierto"},
        headers={"Authorization": f"Bearer {citizen2_token}"}
    )
    assert status_unauth.status_code == 403

