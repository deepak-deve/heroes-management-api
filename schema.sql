CREATE DATABASE IF NOT EXISTS heroes_db;

USE heroes_db;

CREATE TABLE IF NOT EXISTS heroes(
    name VARCHAR(50),
    skill VARCHAR(50),
    rank INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password TEXT
);
