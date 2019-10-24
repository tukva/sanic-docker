from engine import Engine


async def prepare_db(app, loop):
    await Engine.init()
