from fastapi import FastAPI
from typing import Optional

app = FastAPI()

#home route
@app.get("/")
def index():
    return {"Data":{"name":"Aditya Urkude","age":23}}


#passing id to func
@app.get("/about/{id}")
def about(id):
    return {"id":id}


#passing id as int to func
@app.get("/blog/{id}")
def about(id:int):
    return {"id":id}

# query parms
@app.get("/stories")
def stories(limit=10, valid:bool = False, sort:Optional[str]= None):
    if valid:
        return {"data":f"{limit} valid stoires in blogs"}
    else:
        return {"data":f"{limit} invalid stoires in blogs"}

