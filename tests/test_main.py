# test_main.py

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

import sys
import os

# 현재 스크립트 파일의 경로를 얻어옴
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 디렉토리를 계산
project_root = os.path.abspath(os.path.join(current_dir, ".."))
# sys.path에 프로젝트 루트 디렉토리를 추가
sys.path.insert(0, project_root)

from app.main import app, init
from app.schema import Item

@pytest.fixture(scope="module")
def test_db():
    db = AsyncSession()
    yield db
    db.close()

@pytest.fixture(autouse=True, scope="module")
async def initialize_test_db(test_db):
    await init()

def test_create_item_with_testclient(test_db):
    item_data = {
        "created": "2023-11-10T12:34:56",
        "name": "test 1",
        "content": "MTIzNDU="
    }
    update_item_data = {
        "created": "2023-11-10T12:34:56",
        "name": "update name",
        "content": "MTIzNDU="
    }
    delete_success = {
        "message": "Item deleted successfully"
    }

    with TestClient(app) as client:
        # /create/{id} 엔드포인트에 post 요청 보내기
        response = client.post("/create", json=item_data)
        assert response.status_code == 200
        created_item = response.json()
        assert created_item["created"] == item_data["created"]
        assert created_item["name"] == item_data["name"]
        assert created_item["content"] == item_data["content"]

        # 생성된 아이템의 id 값을 가져옴
        item_id = created_item["id"]

        # /read/{id} 엔드포인트에 GET 요청 보내기
        response_read = client.get(f"/read/{item_id}")
        assert response_read.status_code == 200
        read_item = response_read.json()
        assert read_item["created"] == item_data["created"]
        assert read_item["name"] == item_data["name"]
        assert read_item["content"] == item_data["content"]

        # /update/{id} 엔드포인트에 PUT 요청 보내기
        response = client.put(f"/update/{item_id}", json=update_item_data)
        assert response.status_code == 200
        update_item = response.json()
        assert update_item["id"] == item_id
        assert update_item["created"] == update_item_data["created"]
        assert update_item["name"] == update_item_data["name"]
        assert update_item["content"] == update_item_data["content"]

        # /delete/{id} 엔드포인트에 DELETE 요청 보내기
        response = client.delete(f"/delete/{item_id}")
        assert response.status_code == 200
        delete_item = response.json()
        assert delete_item["message"] == delete_success["message"]

