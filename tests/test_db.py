import os

from dotenv import load_dotenv
import pytest
from tortoise import Tortoise

from db.db import init
from db.models import User, Goal, Transaction

load_dotenv()


@pytest.fixture
@pytest.mark.asyncio
async def db():
    db_url = os.getenv("TEST_DATABASE_URL",
                       "sqlite://:memory:")
    await init(db_url)
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_create_objects(db):
    assert await User.all().count() == 0
    await User.create(username="bob", password="changeme")
    assert await User.all().count() == 1
    user = await User.first()
    assert user.username == "bob"
    assert user.password == "changeme"
    await user.delete()
    assert await User.all().count() == 0
