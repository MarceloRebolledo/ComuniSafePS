import uuid
import httpx
import logging
from app.config import settings

logger = logging.getLogger("comunisafe")
logging.basicConfig(level=logging.INFO)

async def dispatch_report_to_municipality(
    report_id: int,
    title: str,
    description: str,
    category: str,
    latitude: float,
    longitude: float,
    address: str,
    severity: str,
    reporter_name: str,
    reporter_email: str
) -> str:
    """
    Simulates sending a report's data to the municipality API.
    Prints the payload to the console and makes a mock HTTP request.
    If the request succeeds (or fails/timeouts), it generates and returns a 
    fictitious unique ticket ID to display in the frontend.
    """
    payload = {
        "report_id": report_id,
        "title": title,
        "description": description,
        "category": category,
        "latitude": latitude,
        "longitude": longitude,
        "address": address,
        "severity": severity,
        "reporter_name": reporter_name,
        "reporter_email": reporter_email
    }
    
    ticket_id = f"MUNI-TICKET-{uuid.uuid4().hex[:6].upper()}"
    
    print("\n==================================================")
    print("=== MOCK MUNICIPALITY DISPATCH SYSTEM ===")
    print(f"Despachando incidencia {report_id} a URL: {settings.MUNICIPALITY_API_URL}")
    print(f"Payload enviado: {payload}")
    
    # Try calling the API. In a mock/classroom scenario, this might fail, 
    # but we catch exceptions so the app keeps functioning and returns the ticket.
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.post(settings.MUNICIPALITY_API_URL, json=payload)
            print(f"Respuesta real del servidor municipal: Status {response.status_code}")
    except httpx.RequestError as exc:
        print(f"Servidor municipal no disponible (Simulación activada): {exc}")
    
    print(f"Ticket Municipal asignado: {ticket_id}")
    print("==================================================\n")
    
    return ticket_id
