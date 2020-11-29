from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from schema import schema_generated
from controller import controller_generated
from database import get_db


router = APIRouter()


@router.post("/generated", response_model=schema_generated.Generated, tags=["generated"])
async def create_generated(generated: schema_generated.Generated, db: Session = Depends(get_db)):
    return controller_generated.create_generated(db, generated)


@router.get("/generated/{id}", response_model=schema_generated.Generated, tags=["generated"])
async def get_generated(id: int, db: Session = Depends(get_db)):
    db_generated = controller_generated.get_generated(db, id)
    if db_generated is None:
        raise HTTPException(status_code=404, detail="generated not found")
    return db_generated


@router.get("/generated", response_model=List[schema_generated.Generated], tags=["generated"])
async def get_all_generated(db: Session = Depends(get_db)):
    all_db_generated = controller_generated.get_all_generated(db)
    if all_db_generated is None:
        raise HTTPException(status_code=404, detail="0 generated found, empty table")
    return all_db_generated


@router.put("/generated/{id}", tags=["generated"])
async def update_generated(id: int, field_name: str, field_value: str, db: Session = Depends(get_db)):
    try:
        db_generated = controller_generated.update_generated(db, id, field_name, field_value)
        if db_generated is None:
            raise HTTPException(status_code=404, detail="generated not found")
        return db_generated
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/generated/{id}", tags=["generated"])
async def delete_generated(id: int, db: Session = Depends(get_db)):
    controller_generated.delete_generated(db, id)
