import asyncio
import os

from dotenv import load_dotenv
from tortoise import Tortoise
import pytest

from db.db import init, create_user, create_goal, add_transaction
from db.models import Transaction, TransactionType

load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True, scope="session")
@pytest.mark.asyncio
async def db():
    db_url = os.getenv("TEST_DATABASE_URL",
                       "sqlite://:memory:")
    await init(db_url)
    yield
    await Tortoise.close_connections()


@pytest.fixture
@pytest.mark.asyncio
async def user():
    user = await create_user("bob", "changeme")
    yield user
    await user.delete()


@pytest.fixture
@pytest.mark.asyncio
async def goal(user):
    goal = await create_goal("ipad", 379, user)
    yield goal
    await goal.delete()


@pytest.fixture
@pytest.mark.asyncio
async def transactions(goal):
    amounts = (10, 150, 125)
    transaction_types = (
        TransactionType.SAVING,
        TransactionType.DONATION,
        TransactionType.OTHER)
    concepts = ("pocket money", "grandma", "mom and dad bday")
    for amount, transaction_type, concept in zip(
        amounts, transaction_types, concepts
    ):
        await add_transaction(goal, transaction_type, amount, concept)
    yield
    await Transaction.all().delete()
