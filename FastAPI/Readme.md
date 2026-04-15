* FastAPI → handles requests
* SQLAlchemy → interacts with DB
* Pydantic → validates data
* Uvicorn → runs the server

Client → Uvicorn → FastAPI → Pydantic → CRUD → SQLAlchemy → DB
                                   ↑
                              Response Model

from fastapi import FastAPI, Depends, HTTPException
FastAPI => to create the API app
Depends => dependency injection. Example: Creation of a single session id and injecting it over the code.
HTTPException => to format proper errors

from sqlalchemy.orm import Session
* Session : temp db connection

import models, schemas, crud
* models : defines db tables
* schemas : defines API input and output formats
* CRUD : db logics (create, get, post, put, delete)

from database import engine, SessionLocal, Base
This happens in the db configuration layer
* engine : to connect to the db
* SessionLocal : to create Local Session
* Base : Base class for all the models