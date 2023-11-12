# model.py
from .database import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime, LargeBinary
from datetime import datetime

class Item(Base):
    __tablename__ = "Item"
    id = Column(Integer, primary_key = True, autoincrement = True)
    created = Column(DateTime, default=datetime.utcnow)
    name = Column(String)
    # content 필드의 데이터 크기가 10MB 이상인 데이터를 저장할 수 있다고 대비
    content = Column(LargeBinary)