from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_nonempty_request():
    r=client.post('/process',json={'message':'case.created'})
    assert r.status_code==200
    assert r.json()['status']=='accepted'
def test_rejects_empty_request():
    assert client.post('/process',json={'message':''}).status_code==422
def test_step_signature_fixture():
    from app.features.step_2 import transform
    assert len(transform('case.created')) == 64
def test_step_dedupe_fixture():
    from app.features.step_3 import transform
    assert len(transform('a'*64)) == 16
def test_step_notification_fixture():
    from app.features.step_4 import transform
    assert transform('abc') == 'mock_notification:abc'
