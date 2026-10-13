# STEP-5 — Test replay and failures

This branch implements `POST /webhooks` with constant-time HMAC signature verification, a timestamp replay window, SQLite event ID deduplication and a mock notification response.

Run `pip install -r requirements.txt` then `pytest -q`; provide `WEBHOOK_SECRET` only through environment configuration. The test suite verifies signature rejection, stale replay, invalid data and duplicate event handling.

The mock notifier is deliberately not a real delivery service. Production work still requires transactional outbox and tenant separation.

## Database (Entity) Relations
STEP-5 introduces SQLite table `delivered` via `record_once` in `app/features/webhook.py`: one `event_id TEXT PRIMARY KEY` field used to reject duplicates. `STEP-5.erd` captures the exact table. The main `.inkp` has tab `STEP-5-ERD`. Prior steps do not persist webhook events; no fictional tables or relations exist.
