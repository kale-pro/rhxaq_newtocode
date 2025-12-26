CREATE DATABASE task_manager;
USE task_manager;

-- USERS TABLE
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

-- PROJECTS TABLE
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- TASKS TABLE
CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status ENUM('pending', 'in_progress', 'done') NOT NULL,
    created_at DATE NOT NULL,
    due_date DATE NOT NULL,
    project_id INT NOT NULL,

    CONSTRAINT fk_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE,

    -- REAL-WORLD RULE
    CONSTRAINT chk_due_date
        CHECK (due_date >= created_at)
);
select* from users,projects,tasks;

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY '654321';
FLUSH PRIVILEGES;
