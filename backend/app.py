from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import redis
import os

app = Flask(__name__)

metrics = PrometheusMetrics(app)
# PostgreSQL connection
db_conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():

    # Redis cache check
    cached = redis_client.get("homepage")

    if cached:
        return jsonify({
            "source": "redis-cache",
            "message": cached
        })

    # PostgreSQL query
    cur = db_conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id SERIAL PRIMARY KEY,
            message TEXT
        )
    """)

    cur.execute("""
        INSERT INTO visitors (message)
        VALUES ('ResilioOps Visitor Connected')
    """)

    db_conn.commit()

    cur.execute("SELECT COUNT(*) FROM visitors")
    count = cur.fetchone()[0]

    message = f"Visitor count: {count}"

    # Save to Redis
    redis_client.set("homepage", message)

    cur.close()

    return jsonify({
        "source": "postgresql",
        "message": message
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
