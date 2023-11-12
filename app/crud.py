# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from . import schema, models
from sqlalchemy.future import select  # 이 부분을 추가해 주세요
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
# Read 요청이 많을 것을 대비하여 캐시를 사용해 개발
from functools import lru_cache

async def create_item(db: AsyncSession, item: schema.Item):
    item_model = models.Item(**item.dict())
    async with db.begin():
        db.add(item_model)
    await db.refresh(item_model)
    
    return item_model

@lru_cache(maxsize=128)  # 최근 128개의 요청 결과 메모리에 유지
async def read_item(db: AsyncSession, id: int):
    async with db.begin():
        result = await db.execute(select(models.Item).where(models.Item.id == id))
        item = result.scalar()
        if item is None:
            raise HTTPException(status_code=404, detail="id not exist")
    return item

async def update_item(db: AsyncSession, id: int, item: schema.Item):
    async with db.begin():
        result = await db.execute(select(models.Item).where(models.Item.id == id))
        item_to_update = result.scalar()

        if item_to_update:
            for key, value in item.dict().items():
                setattr(item_to_update, key, value)
    await db.commit()
    await db.refresh(item_to_update)

    return item_to_update

async def delete_item(db: AsyncSession, id: int):
    async with db.begin():
        result = await db.execute(select(models.Item).where(models.Item.id == id))
        item = result.scalar()

        if item:
            await db.delete(item)
            
    await db.commit()

    return {"message": "Item deleted successfully"}

async def error_message(message):
    return {"error": message}

# 확인용
async def get_item(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(models.Item))
        items = result.scalars().all()
        if not items:
            raise HTTPException(status_code=404, detail="not exist")
    return items