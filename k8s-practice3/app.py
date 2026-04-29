import os
import time

from flask import Flask
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)


def db_config():
    return {
        "host": os.getenv("DB_HOST", "practice3-postgres"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "appdb"),
        "user": os.getenv("DB_USER", "appuser"),
        "password": os.getenv("DB_PASSWORD", "apppassword"),
    }


def get_connection(retries=10, delay=2):
    last_error = None

    for _ in range(retries):
        try:
            return psycopg2.connect(**db_config())
        except psycopg2.OperationalError as error:
            last_error = error
            time.sleep(delay)

    raise last_error


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    visitor_name TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
                """
            )
        conn.commit()


@app.route("/")
def index():
    name = os.getenv("NAME", "artur")

    init_db()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO visits (visitor_name) VALUES (%s) RETURNING id, created_at;",
                (name,),
            )

            cur.execute("SELECT COUNT(*) AS total FROM visits;")
            total = cur.fetchone()["total"]

            cur.execute(
                """
                SELECT id, visitor_name, created_at
                FROM visits
                ORDER BY created_at DESC
                LIMIT 5;
                """
            )
            visits = cur.fetchall()

        conn.commit()

    items = ""

    for visit in visits:
        created_at = visit["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        items += f"<li>#{visit['id']} — Hello {visit['visitor_name']} — {created_at}</li>"

    return f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>K8S Practice 3</title>
      </head>
      <body>
        <h1>Hello {name}</h1>
        <h2>PostgreSQL is connected</h2>
        <p>Total visits saved in database: <strong>{total}</strong></p>
        <h3>Last visits:</h3>
        <ul>
          {items}
        </ul>
      </body>
    </html>
    """


@app.route("/health")
def health():
    try:
        with get_connection(retries=1, delay=1) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")

        return {"status": "ok", "database": "connected"}
    except Exception as error:
        return {
            "status": "error",
            "database": "disconnected",
            "message": str(error),
        }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)