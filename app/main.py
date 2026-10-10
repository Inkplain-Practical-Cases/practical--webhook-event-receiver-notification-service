"""HTTP door for signed SaaS webhook events.
ICS layer: door.
Why it exists: validates raw request signatures before changing delivery state.
Without it: unauthenticated callbacks could reach business processing.
"""
import json
from fastapi import FastAPI, Header, HTTPException, Request
from app.features.webhook import verify_signature, parse_event, check_timestamp, record_once, notify
app = FastAPI(title="Webhook Event Receiver & Notification Service")

@app.post("/webhooks")
async def receive_webhook(request: Request, x_webhook_signature: str = Header(default="")) -> dict:
    """Authenticate raw bytes, validate event identity and prevent duplicate side effects."""
    body = await request.body()
    if len(body) > 65536:
        raise HTTPException(status_code=413, detail="event too large")
    if not verify_signature(body, x_webhook_signature):
        raise HTTPException(status_code=401, detail="invalid signature")
    try:
        event = parse_event(body)
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=422, detail="invalid event") from exc
    if not check_timestamp(event):
        raise HTTPException(status_code=401, detail="stale event")
    if not record_once(event["id"]):
        return {"status": "duplicate", "event_id": event["id"]}
    return {"status": "accepted", "notification": notify(event)}
