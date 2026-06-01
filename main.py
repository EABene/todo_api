from fastapi import FastAPI

app = FastAPI() # erzeugt App


@app.get("/")
def read_root():
    return {"message": "Hello World"}