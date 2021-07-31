import pytest

from db.db import (create_user, delete_user,
                   create_goal, delete_goal,
                   amount_saved, add_transaction)
from db.models import User, Goal, Transaction, TransactionType
from db.encryption import verify_password
from db.exceptions import (UserExists, UserDoesNotExist,
                           DuplicatedGoal, GoalDoesNotExist,
                           InsufficientFunds)


@pytest.mark.asyncio
async def test_create_user(user):
    username = "bob"
    assert str(user) == username
    assert verify_password("changeme", user.password) is True
    err = "Username bob already exists"
    with pytest.raises(UserExists, match=err):
        await create_user(username, "some_pass")


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
        other_goal_id = goal.id + 1
        await delete_goal(other_goal_id, user)
    await delete_goal(goal.id, user)
    goal_count = await Goal.filter(user=user).count()
    assert goal_count == 0


@pytest.mark.asyncio
async def test_adding_transactions(goal, transactions):
    transaction_count = await Transaction.all().count()
    assert transaction_count == 3
    total_saved = await amount_saved(goal)
    assert total_saved == 285


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(goal, transactions):
    err = ("Cannot withdraw - saved: 285.0, but need"
           " 379.0 for ipad goal.")
    with pytest.raises(InsufficientFunds, match=err):
        await add_transaction(goal, TransactionType.WITHDRAWAL)


@pytest.mark.asyncio
async def test_withdraw_sufficient_funds(goal, transactions):
    await add_transaction(goal, TransactionType.DONATION,
                          100, "Oli did some serious work")
    await add_transaction(goal, TransactionType.WITHDRAWAL)
    assert goal.achieved is True
    total_saved = await amount_saved(goal)
    assert total_saved == 6.0
    transactions = await Transaction.all()
    actual = [str(tr) for tr in transactions]
    expected = [
        "10.0 (TransactionType.SAVING)",
        "150.0 (TransactionType.DONATION)",
        "125.0 (TransactionType.OTHER)",
        "100.0 (TransactionType.DONATION)",
        "-379.0 (TransactionType.WITHDRAWAL)",
    ]
    assert actual == expected
    assert transactions[-1].concept == "withdrawal for ipad goal"
