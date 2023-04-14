from fastapi import Depends, FastAPI, HTTPException,APIRouter
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .schemas  import Response,CreateUser,CreateItem,UserBase
from .database import SessionLocal, engine

route = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@route.get("/users/")
def find_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        users = crud.get_all_users(db= db, skip=skip, limit=limit)
        return Response(code= 200,status= 'OK',message= 'Tìm user thành công',result = users).dict(exclude_none=True)
    except:
        return HTTPException(status_code=404, detail="Không có user ")
@route.get("/users/{id}")
def find_user_id(user_id: int , db: Session = Depends(get_db)):
    user = crud.get_user_id(db = db,user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return Response(code= 200,status= 'OK',message= 'Tìm user ID {} thành công'.format(user_id),result = user).dict(exclude_none=True)

@route.post("/user/create")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db= db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email đăng kí đã tồn tại")
    user = crud.create_user(db=db, user=user)
    return Response(code= 200,status= 'OK',message= 'Tạo user thành công',result = user).dict(exclude_none=True)

@route.post("/user/update")
async def update_user(user: UserBase, db: Session = Depends(get_db)):
    user = crud.update_user(db,user_id = user.id,
                            username = user.username,
                            email = user.email,
                            password=user.password,
                            gender= user.gender)
    return Response(code= 200, status= 'OK',message= 'Sửa user thành công',result = user).dict(exclude_none=True)

@route.delete("/user/delete/{id}")
async def delete_user(user_id : int, db: Session = Depends(get_db)):
    try:
        crud.delete_user(db,user_id = user_id)
        return Response(code=200, status='OK', message='Xóa user ID {} thành công'.format(user_id)).dict(exclude_none=True)
    except:
        return HTTPException(status_code=404, detail="Không tìm thấy user ID {}".format(user_id))

@route.get("/items/")
def find_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        items = crud.get_all_items(db, skip=skip, limit=limit)
        return Response(code= 200,status= 'OK',message= 'Tìm Item thành công',result = items).dict(exclude_none=True)
    except:
        return HTTPException(status_code=404, detail="Lỗi khi tìm Item")

@route.post("/users/{user_id}/items/")
def create_item_for_user(user_id: int, item: CreateItem, db: Session = Depends(get_db)):
    user = crud.get_user_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    else:
        item = crud.create_item_user(db=db, item=item, user_id=user_id)
        return Response(code=200, status='OK', message='Thêm item cho UserID {} thành công'.format(user_id),result=item).dict(exclude_none=True)

@route.get('/user/search')
def search_user(query:str,db: Session = Depends(get_db)):
    return crud.search_user(query=query,db=db)

