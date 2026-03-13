# Heroes Management API

Backend project built using Python, Flask and MySQL.

Features:
- Hero CRUD operations
- Web interface using Flask templates
- REST API
- User authentication (Register / Login)
- Password hashing using bcrypt

Technologies:
- Python
- Flask
- MySQL
- bcrypt

Setup:

1. Create database

mysql -u root -p < schema.sql

2. Install requirements

pip install -r requirements.txt

3. Run the server

python A25MYSQL+Auth.py

Server runs at:
http://127.0.0.1:5000

> ⚠️ Note: `heroes.db` (SQLite) or MySQL data is **not included**. You can create the database using `schema.sql`.

View the project on GitHub: [https://github.com/deepak-deve/heroes-management-api](https://github.com/deepak-deve/heroes-management-api)
