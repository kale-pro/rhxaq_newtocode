from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

STATE_FILE = "state.json"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
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
    data = request.json

    # BACKEND VALIDATION (blocks bad input)
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    if data["status"] not in ["pending", "in_progress", "done"]:
        return jsonify({"error": "Invalid status"}), 400

    if data["due_date"] < data["created_at"]:
        return jsonify({"error": "Due date cannot be before created date"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks (title, status, created_at, due_date, project_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["title"],
            data["status"],
            data["created_at"],
            data["due_date"],
            data["project_id"]
        ))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cur.close()
        conn.close()

    update_state()
    return jsonify({"message": "Task added successfully"}), 201


@app.route("/tasks")
def get_tasks():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(debug=True)
