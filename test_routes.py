from werkzeug.security import generate_password_hash

from app import app, get_local_user, save_local_user, ensure_database_schema


def test_database_schema_helper_exists():
    assert callable(ensure_database_schema)


def test_local_user_persistence_helpers():
    user = save_local_user("Persist User", "persist@example.com", generate_password_hash("pass123"), "user")
    assert user is not None
    assert get_local_user("PERSIST@EXAMPLE.com")["name"] == "Persist User"


client = app.test_client()
for path in ['/', '/buses', '/login', '/register', '/history', '/admin']:
    try:
        resp = client.get(path)
        print(path, resp.status_code)
    except Exception as e:
        print('ERROR', path, type(e).__name__, e)
