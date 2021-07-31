import pytest

from db.db import create_user, delete_user, create_goal, delete_goal
from db.models import User, Goal
from db.encryption import verify_password
from db.exceptions import (UserExists, UserDoesNotExist,
                           DuplicatedGoal, GoalDoesNotExist)


@pytest.mark.asyncio
async def test_create_user(user, login):
    username, password = login
    assert str(user) == username
    assert verify_password(password, user.password) is True
    err = "Username bob already exists"
    with pytest.raises(UserExists, match=err):
        await create_user(username, password)


@pytest.mark.asyncio
async def test_delete_user(user):
    err = "Username bob2 does not exist"
    with pytest.raises(UserDoesNotExist, match=err):
        await delete_user("bob2")
    ret = await delete_user("bob")
    assert ret is None
    user_count = await User.all().count()
    assert user_count == 0


@pytest.mark.asyncio
async def test_create_goal(user, goal):
    assert goal.description == "ipad"
    err = "You already added.*new one."
    with pytest.raises(DuplicatedGoal, match=err):
        await create_goal("ipad", 379, user)
    await create_goal("ipad2", 379, user)
    goal_count = await Goal.filter(user=user).count()
    assert goal_count == 2


@pytest.mark.asyncio
async def test_delete_goal(user, goal):
    err = "Goal does not exist for user"
    goal_count = await Goal.filter(user=user).count()
    assert goal_count == 1
    with pytest.raises(GoalDoesNotExist, match=err):
        await delete_goal(2, user)
    await delete_goal(1, user)
    goal_count = await Goal.filter(user=user).count()
    assert goal_count == 0
