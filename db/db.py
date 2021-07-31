import os

from dotenv import load_dotenv
from tortoise import Tortoise, run_async

from .models import (User, Goal,
                     Transaction,
                     TransactionType)
from .encryption import get_password_hash
from db.exceptions import (UserExists, UserDoesNotExist,
                           DuplicatedGoal, GoalDoesNotExist,
                           InsufficientFunds)

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


async def create_goal(description, amount, user):
    goal, created = await Goal.get_or_create(
        description=description,
        amount=amount,
        user=user)
    if created:
        return goal
    else:
        raise DuplicatedGoal(
            ("You already added this goal, delete it"
             " or create a new one.")
        )


async def delete_goal(goal_id, user):
    goal = await Goal.get_or_none(
        pk=goal_id,
        user=user)
    if goal is None:
        raise GoalDoesNotExist("Goal does not exist for user")
    await goal.delete()
    return None


async def amount_saved(goal):
    transactions = await Transaction.filter(
        goal=goal,
    ).all()
    return sum(tr.amount for tr in transactions)


async def add_transaction(goal, transation_type,
                          amount=0, concept=''):
    if transation_type == TransactionType.WITHDRAWAL:
        amount = goal.amount
        saved = await amount_saved(goal)
        if amount > saved:
            raise InsufficientFunds(
                (f"Cannot withdraw - saved: {saved}, but need"
                 f" {amount} for {goal.description} goal."))
        amount *= -1

    transaction = await Transaction.create(
        amount=amount,
        transation_type=transation_type,
        goal=goal,
        concept=concept)

    goal.achieved = True
    await goal.save()

    return transaction


if __name__ == "__main__":  # pragma: no cover
    run_async(init())
