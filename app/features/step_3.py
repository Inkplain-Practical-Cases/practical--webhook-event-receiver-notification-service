"""STEP-3: Deduplicate validated events.
ICS layer: service. Called by: app.main.process.
Why it exists: isolates this teaching operation for direct tests.
Without it: the specific STEP-3 transformation is unavailable.
"""
def transform(value:str)->str:
    """Transform a synthetic string into an offline result."""
    import hashlib
    return hashlib.sha256(value.encode()).hexdigest()[:16]
