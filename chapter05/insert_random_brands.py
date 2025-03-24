import os
import asyncio
from random import sample
import asyncpg

from chapter05 import load_common_words


def generate_brand_names(words: list[str]) -> list[tuple[str]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    sql = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(sql, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password=os.getenv('DB_PASSWORD')
    )
    await insert_brands(common_words, connection)


asyncio.run(main())
