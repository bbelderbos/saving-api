import os

from dotenv import load_dotenv
from tortoise import Tortoise
import pytest

from db.db import init, create_user

load_dotenv()


@pytest.fixture
@pytest.mark.asyncio
async def db():
    db_url = os.getenv("TEST_DATABASE_URL",
                       "sqlite://:memory:")
    await init(db_url)
    yield
    await Tortoise.close_connections()


@pytest.fixture
def login():
    return ("bob", "changeme")


@pytest.fixture
@pytest.mark.asyncio
async def user(login):
    username, password = login
    user = await create_user(username, password)
    return user
