from fastapi import FastAPI,status,HTTPException,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .database import engine,get_db
from typing import List
from . import models,schemes,utils
from fastapi.middleware.cors import CORSMiddleware
from .routers import user,post,auth,vote
#   make sqlalcgemy to create tables 
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)     
app.include_router(post.router)     
app.include_router(auth.router)
app.include_router(vote.router)     
@app.get("/")
def root():
    return {"test":"ok done"}
