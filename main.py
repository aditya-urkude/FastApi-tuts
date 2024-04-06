from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
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

# query parms, default value, optional parms
@app.get("/stories")
def stories(limit=10, valid:bool = False, sort:Optional[str]= None):
    if valid:
        return {"data":f"{limit} valid stoires in blogs"}
    else:
        return {"data":f"{limit} invalid stoires in blogs"}


# request body 
class Blog(BaseModel):
    title : str
    body : str
    published_at: Optional[bool]


@app.post("/create")
def crate_blog(request: Blog):
    return f"My {request.title} is created"


# # to chnage port 
# if __name__ == "__main__":
#     uvicorn.run(app, host= "127.0.0.1", port = 9000)