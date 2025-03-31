import os
import logging
import asyncio
import asyncpg
from asyncpg.transaction import Transaction


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password=os.getenv('DB_PASSWORD')
    )
    transaction: Transaction = connection.transaction()
    await transaction.start()

    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(1, 'brand_XXX')")
    except asyncpg.PostgresError:
        logging.exception("Error while running transaction")
        await transaction.rollback()
    else:
        print("Transaction was successful")
        await transaction.commit()

    query = """SELECT brand_name FROM brand WHERE brand_name = 'brand_XXX'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())
