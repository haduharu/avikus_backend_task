# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 테스트 환경인지 여부를 확인합니다.
IS_TEST_ENV = os.getenv("TEST_ENV", "false").lower() == "true"

# 연결 정보를 설정합니다.
if IS_TEST_ENV:
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://test_username:test_password@test_db:5432/test_items"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://username:password@db:5432/items"

# 비동기 엔진을 생성합니다.
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# 비동기 세션을 생성합니다.
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


