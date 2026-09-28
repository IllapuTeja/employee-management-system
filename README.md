# Employee Management System

A mini project built with Python, MySQL, and Tkinter for managing employee records.

Features:
- Add employee
- Update employee
- Delete employee
- Search employee
- View all employees
- Clear form fields
- MySQL database integration

Project structure:
- `app.py` – Tkinter GUI
- `db_config.py` – database settings
- `employee_db.py` – MySQL CRUD operations
- `requirements.txt` – Python dependencies

Setup:
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start MySQL and ensure a user is available.
3. Update your MySQL credentials in `db_config.py`.
4. Run the app:
   ```bash
   python app.py
   ```

Default database config:
- Host: localhost
- User: root
- Password: ""
- Database: employee_management

If MySQL is not running, the app will not connect until the database service is started.
