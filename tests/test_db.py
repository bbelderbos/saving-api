import pytest

from db.db import create_user, delete_user
from db.models import User
from db.encryption import verify_password
from db.exceptions import UserExists, UserDoesNotExist


@pytest.mark.asyncio
async def test_create_objects(db):
    await User.create(username="bob", password="changeme")
    user_count = await User.all().count()
    assert user_count == 1

    user = await User.first()
    assert user.username == "bob"
    assert user.password == "changeme"

    await user.delete()
    user_count = await User.all().count()
    assert user_count == 0


@pytest.mark.asyncio
async def test_create_user(db):
    username, password = "bob", "changeme"
    user = await create_user(username, password)
    assert user.username == username
    assert verify_password(password, user.password) is True
    err = "Username bob already exists"
    with pytest.raises(UserExists, match=err):
        await create_user(username, password)


@pytest.mark.asyncio
async def test_delete_user(db):
    username, password = "bob", "changeme"
    user = await create_user(username, password)
    err = "Username bob2 does not exist"
    with pytest.raises(UserDoesNotExist, match=err):
        await delete_user("bob2")
    ret = await delete_user(username)
    assert ret is None
    user_count = await User.all().count()
    assert user_count == 0
