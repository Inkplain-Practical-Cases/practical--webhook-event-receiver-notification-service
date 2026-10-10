"""STEP-2: Verify webhook signature.
ICS layer: service. Called by: app.main.process.
Why it exists: isolates this teaching operation for direct tests.
Without it: the specific STEP-2 transformation is unavailable.
"""
def transform(value:str)->str:
    """Transform a synthetic string into an offline result."""
    import hmac,hashlib
    return hmac.new(b"synthetic-demo-key",value.encode(),hashlib.sha256).hexdigest()
