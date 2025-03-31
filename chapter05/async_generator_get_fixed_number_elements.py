import os
import asyncio
import asyncpg


async def take(generator, n: int):
    n_taken = 0
    async for item in generator:
        if n_taken >= n:
            return
        n_taken += 1
        yield item


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password=os.getenv('DB_PASSWORD')
    )
    async with connection.transaction():
        query = "SELECT product_id, product_name FROM product"
        product_generator = connection.cursor(query)

        async for product in take(product_generator, 5):
            print(product)

        print('Got the first 5 products!')

    await connection.close()


asyncio.run(main())
