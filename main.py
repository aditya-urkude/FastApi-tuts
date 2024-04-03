from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Data":{"name":"Aditya Urkude","age":23}}