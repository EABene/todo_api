from fastapi import FastAPI
from pydantic import BaseModel
import json

class Todo(BaseModel):
    id: int
    title: str
    done: bool = False



app = FastAPI() # erzeugt App

# JSON Funktionen
def save_todos():
    with open("todos.json", "w")as f:
        json.dump([todo.dict() for todo in todos], f)
        # Todos sind Pydantic Objekte. JSON kann das nicht direkt lesen.
        # .dict() wandelt es in ein Dict um, List Comprehension macht das für alle

def load_todos():
    try:
        with open("todos.json", "r") as f:
            data = json.load(f)
            return [Todo(**item) for item in data]
        # umgekehrter Weg. **item enpackt dict in Argumente
        # {"id": 1, "title": "x"} wird zu Todo(id=1, title="x")
    except FileNotFoundError:
        return []
    


todos = load_todos() # JSON laden


# CRUD = Create, Read, Update, Delete, Persistenz--Endpoints

# FastAPI Funktionen

@app.get("/") # Decorator für GET-Requests auf /
def read_root():
    return {"message": "Hello World"} # Dict. FastAPI wandelt es automatisch in JSON um

@app.post("/todos") # POST = wegschicken
def create_todo(todo: Todo): # validiert als gültiges Todo, validiert gegen Pydantic Model
    todos.append(todo) # packt in die Liste
    save_todos() # in JSON speichern
    return todo # return als Bestätigung

@app.get("/todos")
def get_todos():
    return todos

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            save_todos()
            return {"message": "Todo deleted"}
    return {"message": "Todo not found"}

