from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,CHAR
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    gender = Column(String(20))

    item = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    price = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="item")