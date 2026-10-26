"""TaskFlow API - a small task tracker used to demo the DevOps platform."""
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage: data resets when the app restarts.
tasks = []
next_id = 1


@app.get("/")
def index():
    return jsonify(service="taskflow", status="running")


@app.get("/health")
def health():
    # Used by Kubernetes probes and the ALB health check.
    return jsonify(status="ok")


@app.get("/version")
def version():
    # The CI/CD pipeline sets APP_VERSION, so you can see which build is live.
    return jsonify(version=os.getenv("APP_VERSION", "dev"))


@app.get("/tasks")
def list_tasks():
    return jsonify(tasks)


@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        data = {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


@app.patch("/tasks/<int:task_id>")
def complete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify(error="task not found"), 404
    task["done"] = True
    return jsonify(task)


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify(error="task not found"), 404
    tasks.remove(task)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)