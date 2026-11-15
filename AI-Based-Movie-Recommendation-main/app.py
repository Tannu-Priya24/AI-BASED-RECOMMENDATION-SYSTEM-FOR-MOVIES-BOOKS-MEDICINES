import sqlite3
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "flicksy_super_secret_123456"

CORS(app, supports_credentials=True)


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id,name,password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["name"] = user[1]

        return jsonify({"message": "Login success", "name": user[1]})

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/user")
def get_user():
    if "user_id" in session:
        return jsonify({
            "logged_in": True,
            "name": session.get("name")
        })

    return jsonify({"logged_in": False})


@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/")
def home():
    return "FLICKSY Backend Running 🚀"


if __name__ == "__main__":
    app.run(debug=True)