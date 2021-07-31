import pytest

from db.models import User


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
