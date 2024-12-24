from fastapi.testclient import TestClient
from FastAPI_app.main import app

client = TestClient(app)


def test_hello_unknown():
    get_response = client.get("/hello/Vitalya")
    assert get_response.status_code == 200
    assert get_response.json() == {"message": f"Hello Vitalya"}

def test_add_user():
    post_response = client.post(
        "/users",
        json={"name": "pomidor", "age": 777}
    )
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "User pomidor added."}


def test_get_user():
    get_response = client.get("/users/0")
    assert get_response.status_code == 200
    assert get_response.json() == {"message": "name:('pomidor', 777)"}
