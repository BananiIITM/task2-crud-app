from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
import os
import json
import random

# Optional: OpenAI client (only used if API key present)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Load environment variables
load_dotenv()

# --- Database setup ---
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False

# Models for API
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class AutoGenRequest(BaseModel):
    prompt: str
    n: int = 3

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- App setup ---
app = FastAPI(title="Iron Lady - Task2 ToDo App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

# --- CRUD endpoints ---
@app.post("/api/tasks", response_model=TaskRead)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    task = Task(title=task_in.title, description=task_in.description, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/api/tasks", response_model=List[TaskRead])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).order_by(Task.id)).all()
    return tasks

@app.get("/api/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_upd: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_upd.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(task, k, v)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

# --- Optional: AI autogen endpoint ---
@app.post("/api/tasks/autogen", response_model=List[TaskRead])
def autogen_tasks(req: AutoGenRequest, session: Session = Depends(get_session)):
    api_key = os.getenv("OPENAI_API_KEY")

    # If no API key, use fallback
    if not api_key or not OpenAI:
        ideas = [
            {
                "title": f"{req.prompt} - Step {i+1}",
                "description": random.choice([
                    "Research and plan this step",
                    "Prepare resources",
                    "Execute and review progress",
                    "Collaborate with team",
                    "Finalize and document"
                ])
            }
            for i in range(req.n)
        ]
        created = []
        for t in ideas:
            db_task = Task(title=t["title"], description=t["description"], completed=False)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            created.append(db_task)
        return created

    # Try with OpenAI if key is available
    try:
        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Return only a JSON array of {title, description}."},
                {"role": "user", "content": f"Create {req.n} actionable tasks for: {req.prompt}"}
            ],
            temperature=0.7,
            max_tokens=400,
        )

        text = resp.choices[0].message.content.strip()
        tasks_json = json.loads(text)

        created = []
        for t in tasks_json[: req.n]:
            db_task = Task(
                title=t.get("title", "Untitled"),
                description=t.get("description"),
                completed=False
            )
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            created.append(db_task)
        return created

    except Exception as e:
        # If OpenAI fails (quota error, etc.), fallback
        ideas = [
            {"title": f"{req.prompt} - Subtask {i+1}", "description": "Generated via fallback"}
            for i in range(req.n)
        ]
        created = []
        for t in ideas:
            db_task = Task(title=t["title"], description=t["description"], completed=False)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            created.append(db_task)
        return created

# --- Mount static frontend ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")
