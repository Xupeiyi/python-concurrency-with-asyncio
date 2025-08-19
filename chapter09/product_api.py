import os

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool


routes = web.RouteTableDef()
DB_KEY = 'database'


async def create_database_pool(app: Application):
    print('Creating database pool.')
    pool: Pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password=os.getenv('DB_PASSWORD'),
        database='products',
        min_size=6,
        max_size=6
    )
    app[DB_KEY] = pool


async def destroy_database_pool(app: Application):
    print('Destroying database pool.')
    pool: Pool = app[DB_KEY]
    await pool.close()


@routes.get('/brands')
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: list[Record] = await connection.fetch(brand_query)
    results_as_dict: list[dict] = [dict(brand) for brand in results]
    return web.json_response(results_as_dict)


@routes.get('/products/{id}')
async def get_product(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        product_id = int(str_id)
        query = (
            """
            SELECT 
                product_id,
                product_name,
                brand_id
            FROM
                product
            WHERE
                product_id = $1
            """
        )
        connection: Pool = request.app[DB_KEY]
        result: Record = await connection.fetchrow(query, product_id)
        if result is not None:
            return web.json_response(dict(result))
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()


@routes.post('/product')
async def create_product(request: Request) -> Response:
    product_name = 'product_name'
    brand_id = 'brand_id'

    if not request.can_read_body:
        raise web.HTTPBadRequest()

    body = await request.json()

    if product_name in body and brand_id in body:
        db = request.app[DB_KEY]
        await db.execute(
            """
            INSERT INTO 
            product(product_id, product_name, brand_id) 
            VALUES(DEFAULT, $1, $2)
            """,
            body[product_name], int(body[brand_id])
        )
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()


app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)
