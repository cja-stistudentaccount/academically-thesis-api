DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id STRING PRIMARY KEY,
    account_type TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE student_info (
    student_id STRING PRIMARY KEY,
    user_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    age INTEGER,
    address TEXT,
    course TEXT,
    summary TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
