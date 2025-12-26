from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import json
from datetime import datetime
import os

app = Flask(_name_, static_folder='.', static_url_path='')

STATE_FILE = "state.json"


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="654321",
        database="task_manager"
    )


def update_state():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    state = {}

    for table in ["users", "projects", "tasks"]:
        cur.execute(f"SELECT * FROM {table}")
        state[table] = cur.fetchall()

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    cur.close()
    conn.close()


@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    title = data.get("title", "").strip()
    status = data.get("status")
    created_at = data.get("created_at")
    due_date = data.get("due_date")
    project_id = data.get("project_id")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    if status not in ["pending", "in_progress", "done"]:
        return jsonify({"error": "Invalid status"}), 400

    if not created_at or not due_date:
        return jsonify({"error": "created_at and due_date are required"}), 400

    try:
        created_dt = datetime.strptime(created_at, "%Y-%m-%d")
        due_dt = datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    if due_dt < created_dt:
        return jsonify({"error": "Due date cannot be before created date"}), 400

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO tasks (title, status, created_at, due_date, project_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, status, created_at, due_date, project_id)
        )
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": f"DB error: {err}"}), 400
    finally:
        cur.close()
        conn.close()

    update_state()
    return jsonify({"message": "Task added successfully"}), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks ORDER BY task_id DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)


@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(_file_)), "index.html")


if _name_ == "_main_":
    app.run(debug=True)
