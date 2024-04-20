from typing import Annotated, List

from fastapi import Depends, FastAPI
from models.database import engine, session_local
from models.models import Base, Test
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(bind=engine)

def db_connection():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(db_connection)]

@app.post("/{test_id}")
async def add_answers(test_id: int, answers: str):
    db = session_local()
    new_test = Test(test_id, answers)
    db.add(new_test)
    db.commit()

@app.get("/{id}/answers")
async def get_answers(id: int):
    db = session_local()
    return db.query(Test).filter_by(test_id=id).first().answer

@app.put("/{id}")
async def put_results(id: int, result: str = ""):
    db = session_local()
    sample_test = db.query(Test).filter_by(test_id=id).first()
    sample_test.results += result
    db.commit()

@app.get("/{id}/results")
async def get_results(id: int):
    db = session_local()
    return db.query(Test).filter_by(test_id=id).first().results
