"""Offline acceptance tests: authenticity, duplication, replay and validation."""
import hashlib
import hmac
import json
import time
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def signed(event, secret="test-secret"):
    body = json.dumps(event).encode()
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return body, {"X-Webhook-Signature": "sha256=" + digest, "content-type": "application/json"}

def test_verified_event_and_duplicate(monkeypatch, tmp_path):
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")
    monkeypatch.setenv("WEBHOOK_DB_PATH", str(tmp_path / "events.sqlite3"))
    body, headers = signed({"id": "ev-1", "type": "case.created", "timestamp": time.time()})
    assert client.post("/webhooks", content=body, headers=headers).json()["status"] == "accepted"
    assert client.post("/webhooks", content=body, headers=headers).json()["status"] == "duplicate"

def test_invalid_signature(monkeypatch):
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")
    body, headers = signed({"id": "ev-2", "type": "case.created", "timestamp": time.time()}, "wrong")
    assert client.post("/webhooks", content=body, headers=headers).status_code == 401

def test_replay_stale(monkeypatch):
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")
    body, headers = signed({"id": "ev-3", "type": "case.created", "timestamp": time.time() - 900})
    assert client.post("/webhooks", content=body, headers=headers).status_code == 401

def test_invalid_payload(monkeypatch):
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")
    body, headers = signed({"id": "", "type": "case.created", "timestamp": time.time()})
    assert client.post("/webhooks", content=body, headers=headers).status_code == 422
