import os

from dotenv import load_dotenv
from tortoise import Tortoise
import pytest

from db.db import init

load_dotenv()


@pytest.fixture
@pytest.mark.asyncio
async def db():
    db_url = os.getenv("TEST_DATABASE_URL",
                       "sqlite://:memory:")
    await init(db_url)
    yield
    await Tortoise.close_connections()
