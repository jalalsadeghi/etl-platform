import app.main as main_module  # for monkeypatching 'engine'
from app.main import app  # import directly now
from fastapi.testclient import TestClient

client = TestClient(app)


def test_liveness_ok():
    r = client.get("/health/liveness")
    assert r.status_code == 200
    assert r.json() == {"status": "alive"}


def test_readiness_db_ok(monkeypatch):
    class _FakeConn:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def execute(self, *args, **kwargs):
            return 1

    class _FakeEngine:
        def connect(self):
            return _FakeConn()

    monkeypatch.setattr(main_module, "engine", _FakeEngine())
    r = client.get("/health/readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ready"
    assert body["db"] == "ok"


def test_readiness_db_error(monkeypatch):
    class _FailEngine:
        def connect(self):
            raise RuntimeError("cannot connect")

    monkeypatch.setattr(main_module, "engine", _FailEngine())
    r = client.get("/health/readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "degraded"
    assert body["db"] == "error"
    assert "cannot connect" in body["detail"]
