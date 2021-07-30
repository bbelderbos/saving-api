import os

from dotenv import load_dotenv
from tortoise import Tortoise, run_async

load_dotenv()


async def init(db_url=None):
    if db_url is None:
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise RuntimeError("Please specify a DB")

    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())
