from sanic import Sanic
from sanic.response import json
import asyncio
import aiopg

dsn = 'dbname=test user=test password=test host=database'

app = Sanic()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/create-table-user")
async def test(request):
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("CREATE TABLE foo (id serial PRIMARY KEY);")
                await cur.execute("SELECT 1;")
                ret = []
                async for row in cur:
                    ret.append(row)
                assert ret == [(1,)]
    return json({"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
