import os
import asyncpg
import asyncio
from asyncpg import Record


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password=os.getenv('DB_PASSWORD')
    )
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    brand_query = "SELECT brand_id, brand_name FROM brand"
    results: list[Record] = await connection.fetch(brand_query)

    for brand in results:
        print(f"id: {brand['brand_id']}, name: {brand['brand_name']}")

    await connection.close()


asyncio.run(main())
