from sqlalchemy.orm import Session
from schema import generated_schema
from model import generated_model



def get_generated(db: Session, id: int):
    return db.query(generated_model.Generated).filter(generated_model.Generated.id == id).first()


def get_all_generated(db: Session):
    return db.query(generated_model.Generated).all()


def delete_generated(db: Session, id):
    to_delete = db.query(generated_model.Generated).filter(generated_model.Generated.id == id)
    deleted = to_delete.delete()
    if deleted == 0:
        return None
    else:
        db.commit()
        return True


def create_generated(db: Session, generated: generated_schema.Generated):
    db_generated = generated_model.Generated(
        name=generated.name,
        age=generated.age,
    )
    db.add(db_generated)
    db.commit()
    db.refresh(db_generated)
    return db_generated


def update_generated(db: Session, id, field_name, new_value):
    db_generated = db.query(generated_model.Generated).filter(generated_model.Generated.id == id).first()
    setattr(db_generated, field_name, new_value)
    db.commit()
    db.refresh(db_generated)
    return db_generated
