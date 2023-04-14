from sqlalchemy import asc
from sqlalchemy.orm import Session
from .models import User
from . import models, schemas
from .schemas import CreateUser,CreateItem

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).order_by(asc(User.id)).offset(skip).limit(limit).all()

def get_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: CreateUser):
    db_user = User(username= user.username,email= user.email, password= user.password,gender= user.gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session,user_id: int,username: str,email: str,password: str,gender: str):
    _user = get_user_id(db=db,user_id= user_id)
    _user.username = username
    _user.email = email
    _user.password = password
    _user.gender = gender
    db.commit()
    db.refresh(_user)
    return _user

def delete_user(db: Session,user_id: int):
    _user = get_user_id(db=db,user_id= user_id)
    db.delete(_user)
    db.commit()

def search_user(query:str,db: Session):
    result = db.query(User).filter(User.username.contains(query)|User.email.contains(query)).all()
    return result


def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item_user(db: Session, item: CreateItem, user_id: int):
    db_item = models.Item(title= item.title,description= item.description,price= item.price, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


