"""In-memory user store used whenever the database is unreachable, plus
small helpers shared by the register/login routes."""

from werkzeug.security import generate_password_hash, check_password_hash

LOCAL_USERS = {}


def normalize_email(email):
    return (email or "").strip().lower()


def get_local_user(email):
    normalized_email = normalize_email(email)
    if not normalized_email:
        return None
    return LOCAL_USERS.get(normalized_email)


def save_local_user(name, email, password_hash, role="user"):
    normalized_email = normalize_email(email)
    if not normalized_email:
        return None

    existing_user = LOCAL_USERS.get(normalized_email)
    if existing_user:
        existing_user["name"] = name
        existing_user["password"] = password_hash
        existing_user["role"] = role
        return existing_user

    user_id = max((user["user_id"] for user in LOCAL_USERS.values()), default=0) + 1
    user = {
        "user_id": user_id,
        "name": name,
        "email": normalized_email,
        "password": password_hash,
        "role": role
    }
    LOCAL_USERS[normalized_email] = user
    return user


def verify_password(stored_password, submitted_password):
    if not stored_password:
        return False
    try:
        return check_password_hash(stored_password, submitted_password)
    except Exception:
        return stored_password == submitted_password


def seed_default_accounts():
    LOCAL_USERS.setdefault("admin@busgo.com", {
        "user_id": 1,
        "name": "Admin",
        "email": "admin@busgo.com",
        "password": generate_password_hash("admin123"),
        "role": "admin"
    })

    LOCAL_USERS.setdefault("demo@busgo.com", {
        "user_id": 2,
        "name": "Demo User",
        "email": "demo@busgo.com",
        "password": generate_password_hash("demo123"),
        "role": "user"
    })
