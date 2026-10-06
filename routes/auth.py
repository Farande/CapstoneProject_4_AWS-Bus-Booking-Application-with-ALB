from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash

from db import get_db_connection, safe_close, ensure_database_schema
from auth_utils import (
    normalize_email,
    get_local_user,
    save_local_user,
    verify_password,
)

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = normalize_email(request.form.get("email"))
        password = (request.form.get("password") or "").strip()

        if not name or not email or not password:
            return "Please provide all required details"

        hashed_password = generate_password_hash(password)

        if get_local_user(email):
            return "User already exists. Please login."

        connection = get_db_connection()

        if connection is not None:
            try:
                ensure_database_schema()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM Users WHERE email=%s", (email,))
                    if cursor.fetchone():
                        safe_close(connection)
                        return "User already exists. Please login."

                    cursor.execute(
                        """
                        INSERT INTO Users
                        (name, email, password, role)
                        VALUES (%s, %s, %s, 'user')
                        """,
                        (name, email, hashed_password)
                    )
                connection.commit()
                safe_close(connection)
                return redirect("/login")
            except Exception:
                connection.rollback()
                safe_close(connection)

        local_user = save_local_user(name, email, hashed_password, "user")
        if local_user:
            session["user_id"] = local_user["user_id"]
            session["name"] = local_user["name"]
            session["role"] = local_user["role"]
            return redirect("/buses")

        return "Registration failed. Please try again."

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = normalize_email(request.form.get("email"))
        password = (request.form.get("password") or "").strip()

        connection = get_db_connection()
        user = None

        if connection is not None:
            try:
                ensure_database_schema()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Users WHERE email=%s", (email,))
                    user = cursor.fetchone()
            except Exception:
                user = None
            finally:
                safe_close(connection)

        local_user = get_local_user(email)

        if email == "admin@busgo.com" and password == "admin123":
            session["user_id"] = 1
            session["name"] = "Admin"
            session["role"] = "admin"
            return redirect("/admin")

        if email == "demo@busgo.com" and password == "demo123":
            session["user_id"] = 2
            session["name"] = "Demo User"
            session["role"] = "user"
            return redirect("/buses")

        if local_user and verify_password(local_user["password"], password):
            session["user_id"] = local_user["user_id"]
            session["name"] = local_user["name"]
            session["role"] = local_user["role"]
            return redirect("/buses")

        if user and verify_password(user["password"], password):
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")

            return redirect("/buses")

        return "Invalid email or password"

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
