# rhxaq_newtocode
# Task Manager (Flask + MySQL)

A simple web-based *task manager* built with Flask, MySQL, and vanilla JavaScript. It lets you add tasks with status and due dates, stores them in a MySQL database, and displays all tasks in a table on the UI. [file:35][file:36][file:37]

---

## Features

- Create tasks with:
  - Title
  - Status (pending, in_progress, done)
  - Created date
  - Due date
- Store tasks in MySQL with proper foreign keys and a date check constraint. [file:37]
- List all tasks in a table, ordered by latest first. [file:36]
- Basic backend validation and clear error messages. [file:36]
- Simple, clean frontend UI using HTML/CSS/JS. [file:33][file:34][file:35]

---

## Project Structure

- db.py – Flask backend (APIs, DB connection, state export). [file:36]  
- index.html – Main frontend page. [file:35]  
- script.js – Frontend logic for adding/loading tasks. [file:33]  
- style.css – Styling for the UI. [file:34]  
- task_manager.sql – SQL script to create the database, tables, and adjust MySQL auth. [file:37]  
- state.json – Snapshot of current DB state exported by the backend. [file:32]

---

## Setup Instructions

### 1. Clone / copy the project

Place all files in one folder, for example:
