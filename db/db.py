import os

from dotenv import load_dotenv
from tortoise import Tortoise, run_async

from .models import Goal, User, Transaction
from .encryption import get_password_hash
from .exceptions import UserExists, UserDoesNotExist

load_dotenv()


async def init(db_url=None):
    """Initializes database"""
    if db_url is None:
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise RuntimeError("Please specify a DB")

    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models']}
    )
    await Tortoise.generate_schemas()


async def create_user(username, password):
    """Creates user encrypting password, raises exception
       if user already exists"""
    user = await User.get_or_none(
        username=username)
    if user is None:
        encrypted_pw = get_password_hash(password)
        user = await User.create(
            username=username,
            password=encrypted_pw)
        return user
    else:
        raise UserExists(f"Username {username} already exists")


async def delete_user(username):
    user = await User.get_or_none(
        username=username)
    if user is None:
        raise UserDoesNotExist(f"Username {username} does not exist")
    await user.delete()
    return None


if __name__ == "__main__":
    run_async(init())
