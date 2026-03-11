from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "database": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"]
}

redis_client = redis.Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({"app": "Lab5 API", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"db_connection": "successful", "version": version})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)})


@app.route("/cache-test")
def cache_test():
    try:
        redis_client.set("test_key", "redis working")
        value = redis_client.get("test_key")
        return jsonify({"redis": value})
    except Exception as e:
        return jsonify({"redis": "failed", "error": str(e)})


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data["name"]
    email = data["email"]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, email TEXT)"
    )

    cur.execute(
        "INSERT INTO users (name,email) VALUES (%s,%s) RETURNING id",
        (name, email)
    )

    user_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user_id, "name": name, "email": email})


@app.route("/users")
def get_users():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT id,name,email FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)


@app.route("/users/<id>")
def get_user(id):

    cache = redis_client.get(id)

    if cache:
        return jsonify(json.loads(cache))

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT id,name,email FROM users WHERE id=%s", (id,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        user_data = {"id": user[0], "name": user[1], "email": user[2]}
        redis_client.set(id, json.dumps(user_data))
        return jsonify(user_data)

    return jsonify({"error": "User not found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
