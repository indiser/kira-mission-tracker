import os
import hashlib
import secrets
import hmac
from datetime import datetime, timedelta

def hash_password(password: str, salt: bytes = None) -> str:
    """Hash a password using pbkdf2_hmac and a random salt."""
    if salt is None:
        salt = os.urandom(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}${hash_obj.hex()}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    try:
        salt_hex, hash_hex = password_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return hmac.compare_digest(hash_obj.hex(), hash_hex)
    except Exception:
        return False

def generate_session_token() -> str:
    """Generate a secure random session token."""
    return secrets.token_urlsafe(64)

def get_user_by_username(conn, username: str):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cur.fetchone()

def get_user_by_id(conn, user_id: str):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()

def create_session(conn, user_id: str, days=7):
    token = generate_session_token()
    expires_at = datetime.utcnow() + timedelta(days=days)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (%s, %s, %s) RETURNING *",
            (token, user_id, expires_at)
        )
        row = cur.fetchone()
    conn.commit()
    return dict(row)

def get_session(conn, token: str):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE token = %s AND expires_at > NOW()", (token,))
        return cur.fetchone()

def delete_session(conn, token: str):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
    conn.commit()
