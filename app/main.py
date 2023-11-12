# main.py
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .database import AsyncSessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .schema import Item
from . import crud, models, schema

app = FastAPI()

# Swagger UI를 사용할 수 있도록 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/docs", StaticFiles(directory="docs"), name="docs")


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# "Create": 새로운 엔트리를 추가하는 함수 (POST 메서드)
@app.post('/create')
async def post_create_item(item: Item, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, item)

# "Read": 주어진 키에 해당하는 엔트리를 반환하는 함수 (GET 메서드)
@app.get('/read/{id}')
async def get_read_item(id: int, db: AsyncSession = Depends(get_db)):
    read_item = await crud.read_item(db, id)
    if read_item:
        return read_item
    else:
        raise HTTPException(status_code=404, detail="id not exist")

# "Update": 주어진 키에 해당하는 엔트리를 업데이트하는 함수 (PUT 메서드)
@app.put('/update/{id}')
async def put_update_item(item: Item, id: int, db: AsyncSession = Depends(get_db)):
    update_item = await crud.update_item(db, id, item)
    if update_item:
        return update_item
    else:
        raise HTTPException(status_code=404, detail="id not exist")

# "Delete": 주어진 키에 해당하는 엔트리를 삭제하는 함수 (DELETE 메서드)
@app.delete("/delete/{id}")
async def delete_item(id: int, db: AsyncSession = Depends(get_db)):
    read_item = await crud.read_item(db, id)
    if read_item is None:
        raise HTTPException(status_code=404, detail="id not exist")
    else:
        return await crud.delete_item(db, id)