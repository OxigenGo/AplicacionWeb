from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_logout():
    # Simulate a logged-in user by setting the cookie manually (or just calling logout directly since it doesn't strictly require the cookie to be present to attempt deletion, but it's good to check)
    
    # First, let's just call logout and see if it attempts to delete the cookie
    response = client.post("/v1/users/logout")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mensaje": "Sesión cerrada exitosamente"}
    
    # Check that the cookie is deleted in the response headers
    # FastAPI/Starlette deletes cookies by setting Max-Age to 0 or Expires to a past date.
    # We can check 'set-cookie' in headers.
    assert "set-cookie" in response.headers
    assert 'user_data=""' in response.headers["set-cookie"] or "Max-Age=0" in response.headers["set-cookie"]

