function setMessage(text, isError = false) {
    const msg = document.getElementById("message");
    msg.textContent = text;
    msg.className = "message " + (isError ? "error" : "success");
}

function clearForm() {
    document.getElementById("title").value = "";
    document.getElementById("status").value = "pending";
    document.getElementById("created").value = "";
    document.getElementById("due").value = "";
}

function addTask() {
    const title = document.getElementById("title").value;
    const status = document.getElementById("status").value;
    const created = document.getElementById("created").value;
    const due = document.getElementById("due").value;

    fetch("/add-task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: title,
            status: status,
            created_at: created,
            due_date: due,
            project_id: 1
        })
    })
        .then(res => res.json().catch(() => ({})))
        .then(data => {
            if (data.error) {
                setMessage(data.error, true);
            } else {
                setMessage(data.message || "Task added", false);
                clearForm();
                loadTasks();
            }
        })
        .catch(err => {
            setMessage("Request failed: " + err, true);
        });
}

function loadTasks() {
    fetch("/tasks")
        .then(res => res.json())
        .then(tasks => {
            const tbody = document.getElementById("tasks");
            tbody.innerHTML = "";
            tasks.forEach(t => {
                const tr = document.createElement("tr");

                const idTd = document.createElement("td");
                idTd.textContent = t.task_id;

                const titleTd = document.createElement("td");
                titleTd.textContent = t.title;

                const statusTd = document.createElement("td");
                statusTd.textContent = t.status;

                const createdTd = document.createElement("td");
                createdTd.textContent = t.created_at;

                const dueTd = document.createElement("td");
                dueTd.textContent = t.due_date;

                tr.appendChild(idTd);
                tr.appendChild(titleTd);
                tr.appendChild(statusTd);
                tr.appendChild(createdTd);
                tr.appendChild(dueTd);
                tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error("Error loading tasks:", err);
            setMessage("Could not load tasks", true);
        });
}

// run once when page loads
window.onload = loadTasks;
