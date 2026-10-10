# Webhook Event Receiver & Notification Service

Starter offline reference for verified signed callbacks with bounded payloads, 5-minute replay window, atomic SQLite-backed event deduplication, mock notifications and regression tests.

Install with `pip install -r requirements.txt`; set `WEBHOOK_SECRET` (never commit a production secret); execute `pytest -q`; start `uvicorn app.main:app --reload`.

POST `/webhooks` with original JSON body and `X-Webhook-Signature: sha256=<HMAC>` calculated from it. Duplicate event IDs receive status `duplicate`.

**Limitation:** notification delivery is intentionally mocked. For production, implement a transactional outbox and real provider adapter, rate limiting, HTTPS, operational alerting and tenant partitioning. SQLite local storage assumes one shared filesystem.
