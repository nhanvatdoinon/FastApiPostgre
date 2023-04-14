from pydantic import BaseModel, Field
from typing import Optional,TypeVar

from pydantic.generics import GenericModel
from pydantic.schema import Generic

T = TypeVar('T')
class ItemBase(BaseModel):
    id: int
    title: str
    description: str
    price: int
    owner_id: int

    class Config:
        orm_mode = True

class CreateItem(BaseModel):
    title: str
    description: str
    price: int



class UserBase(BaseModel):
    id : Optional[int] = None
    username : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    gender : Optional[str] = None
#    items: list[ItemBase] = []

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[str] = None


class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result : Optional[T]





