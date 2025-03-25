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
    try:
        async with connection.transaction():
            insert_brand_query = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand_query)
            await connection.execute(insert_brand_query)
    except Exception:
        logging.exception("Error while running transaction")
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)
        print(f'Query result was: {brands}')

        await connection.close()


asyncio.run(main())
