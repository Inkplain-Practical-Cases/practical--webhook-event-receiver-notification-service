"""Webhook authentication and delivery logic.
ICS layer: service. Called by: app.main.receive_webhook.
Why it exists: verify signed events and suppress replayed deliveries.
Without it: forged or duplicated events could produce notifications.
"""
import hashlib
import hmac
import json
import os
import sqlite3
import time
from pathlib import Path

def verify_signature(body: bytes, signature: str) -> bool:
    """Compare provider header to the digest of original bytes, in constant time."""
    secret = os.environ.get("WEBHOOK_SECRET", "")
    if not secret or not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature.removeprefix("sha256="))

def parse_event(body: bytes) -> dict:
    """Decode and validate an event shape after verification."""
    value = json.loads(body)
    if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"].strip() or not isinstance(value.get("type"), str) or not value["type"].strip():
        raise ValueError("event id and type required")
    return value

def check_timestamp(value: dict, now: float | None = None) -> bool:
    """Reject stale or future signed events to limit replay exposure."""
    when = value.get("timestamp")
    if isinstance(when, bool) or not isinstance(when, (float, int)):
        return False
    current = time.time() if now is None else now
    return abs(current - when) <= 300

def record_once(event_id: str) -> bool:
    """Atomically remember event identity in a local durable SQLite store."""
    path = Path(os.environ.get("WEBHOOK_DB_PATH", "webhook-events.sqlite3"))
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS delivered (event_id TEXT PRIMARY KEY)")
        result = db.execute("INSERT OR IGNORE INTO delivered(event_id) VALUES (?)", (event_id,))
        return result.rowcount == 1

def notify(event: dict) -> dict:
    """Return a synthetic notification receipt; no external message is sent."""
    return {"delivery": "mock", "event_id": event["id"], "event_type": event["type"]}
