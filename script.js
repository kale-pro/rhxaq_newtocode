function addTask() {
    fetch("/add-task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            title: document.getElementById("title").value,
            status: document.getElementById("status").value,
            created_at: document.getElementById("created").value,
            due_date: document.getElementById("due").value,
            project_id: 1
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        loadTasks();
    });
}

function loadTasks() {
    fetch("/tasks")
        .then(res => res.json())
        .then(tasks => {
            let list = document.getElementById("tasks");
            list.innerHTML = "";
            tasks.forEach(t => {
                let li = document.createElement("li");
                li.textContent = `${t.title} (${t.status})`;
                list.appendChild(li);
            });
        });
}

loadTasks();
