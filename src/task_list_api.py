from fastapi import FastAPI
import task_list

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}