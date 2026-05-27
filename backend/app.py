from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

# PostgreSQL connection
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

# Redis connection
cache = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({
        "message": "ResilioOps Backend Connected",
        "status": "running"
    })

@app.route("/db-test")
def db_test():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    conn.close()

    return jsonify({
        "postgres_version": version[0]
    })

@app.route("/cache-test")
def cache_test():
    cache.set("devops", "resilioops-running")
    value = cache.get("devops")

    return jsonify({
        "redis_value": value
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)