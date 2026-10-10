# STEP-5 — Test replay and failures

This branch implements `POST /webhooks` with constant-time HMAC signature verification, a timestamp replay window, SQLite event ID deduplication and a mock notification response.

Run `pip install -r requirements.txt` then `pytest -q`; provide `WEBHOOK_SECRET` only through environment configuration. The test suite verifies signature rejection, stale replay, invalid data and duplicate event handling.

The mock notifier is deliberately not a real delivery service. Production work still requires transactional outbox and tenant separation.
