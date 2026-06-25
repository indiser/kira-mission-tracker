import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from auth_service import hash_password

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. Please configure .env file.")


def get_connection():
    """Create and return a new psycopg2 database connection."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def run_migrations():
    """Create tables if they do not exist. Called once on app startup."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'paused', 'completed', 'dropped')),
                    priority VARCHAR(20) NOT NULL DEFAULT 'medium'
                        CHECK (priority IN ('low', 'medium', 'high', 'critical')),
                    deadline DATE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    title VARCHAR(255) NOT NULL,
                    is_done BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    token VARCHAR(255) PRIMARY KEY,
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)

            # Seed default admin user if none exists
            cur.execute("SELECT COUNT(*) AS count FROM users")
            if cur.fetchone()["count"] == 0:
                admin_username = os.getenv("ADMIN_USERNAME")
                admin_password = os.getenv("ADMIN_PASSWORD")
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                    (admin_username, hash_password(admin_password))
                )

            # Create or replace the trigger function to auto-update updated_at
            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = NOW();
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)

            # Create trigger only if it does not already exist
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger
                        WHERE tgname = 'set_updated_at'
                          AND tgrelid = 'projects'::regclass
                    ) THEN
                        CREATE TRIGGER set_updated_at
                        BEFORE UPDATE ON projects
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                    END IF;
                END;
                $$;
            """)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
