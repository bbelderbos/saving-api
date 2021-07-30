import os

from dotenv import load_dotenv
import pytest
from tortoise import run_async

from db.db import init
from db.models import User, Goal, Transaction

load_dotenv()


@pytest.fixture
def db():
    db_url = os.getenv("TEST_DATABASE_URL")
    run_async(init(db_url))


def test_init(db):
    assert 1
