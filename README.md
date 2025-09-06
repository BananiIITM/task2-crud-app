# task2-crud-app
Absolutely! Here’s a **professional and informative `README.md`** for your **Task 2 CRUD project**. You can copy-paste it directly into your repo:

```markdown
# Task 2: CRUD Application

A simple **CRUD (Create, Read, Update, Delete) application** built using Python and SQLite, designed as part of Task 2 for the project. This application allows users to manage tasks with a lightweight web interface.

---

## Features

- **Create Tasks:** Add new tasks with a title and description.  
- **Read Tasks:** View all tasks in a list format.  
- **Update Tasks:** Edit existing task details.  
- **Delete Tasks:** Remove tasks when completed or no longer needed.  
- **Mark Tasks as Completed:** Toggle task status easily.  

---

## Technology Stack

- **Backend:** Python (`Flask`)  
- **Database:** SQLite (`todo.db`)  
- **Frontend:** HTML, CSS, JavaScript  
- **Environment:** Virtual environment (`.venv`) for package management  

---

## Project Structure

```

task2-crud-app/
│
├─ app.py                 # Main Flask application
├─ requirements.txt       # Python dependencies
├─ todo.db                # SQLite database
├─ .gitignore             # Ignored files (like .env)
├─ README.md              # Project documentation
├─ LICENSE                # License file
├─ static/
│   ├─ index.html         # Frontend HTML page
│   ├─ style.css          # CSS styles
│   └─ main.js            # JavaScript logic
└─ **pycache**/           # Python cache files

````

---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/BananiIITM/task2-crud-app.git
cd task2-crud-app
````

2. **Create and activate virtual environment**

```bash
python -m venv .venv
& .venv/Scripts/Activate.ps1   # For PowerShell
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

5. **Access in browser**

```
http://127.0.0.1:5000
```

---

## Usage

* Add a task by entering the title and description.
* Tasks are displayed in a list with options to edit, delete, or mark as completed.
* Tasks persist in the `todo.db` SQLite database.

---

## Notes

* Ensure `.env` or any sensitive information **is not pushed** to GitHub.
* This project is built for learning and demonstration purposes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

```

I can also create a **more visually appealing README** with **screenshots and badges** to make it look professional on GitHub.  

Do you want me to do that version too?
```
