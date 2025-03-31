import os
import logging
import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password=os.getenv('DB_PASSWORD')
    )
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as e:
            logging.warning('Ignoring error inserting product color', exc_info=e)

    await connection.close()


asyncio.run(main())
