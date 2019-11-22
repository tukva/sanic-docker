import aiopg.sa

from config import url, DB_POOL_SIZE_MIN, DB_POOL_SIZE_MAX
import aiohttp


class Engine:
    _engine = None

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    async def init(cls):
        cls._engine = await aiopg.sa.create_engine(url,
                                                   minsize=DB_POOL_SIZE_MIN,
                                                   maxsize=DB_POOL_SIZE_MAX)

    @classmethod
    async def acquire(cls):
        return await cls._engine.acquire()

    @classmethod
    async def close(cls):
        cls._engine.close()
        await cls._engine.wait_closed()

    @classmethod
    async def release(cls, connection):
        await  cls._engine.release(connection)


class Connection:
    __slots__ = ('_connection',)

    def __init__(self):
        self._connection = None

    async def __aenter__(self):
        self._connection = await Engine.acquire()
        return self

    async def __aexit__(self, typ, val, trb):
        await Engine.release(self._connection)

    async def execute(self, statement):
        return await self._connection.execute(statement)


class WorkFlowEngine:

    base_url = "http://localhost:8080/engine-rest/engine/default"
    id_process_definition = None
    current_task = None

    async def init(self, name_process_definition):
        process_def_url = f"{self.base_url}/process-definition?name={name_process_definition}"
        async with aiohttp.ClientSession() as session:
            async with session.get(process_def_url) as resp:
                process_def_list = await resp.json()
                self.id_process_definition = process_def_list[0]["id"]
                print(self.id_process_definition)
                await self.set_current_task()

    async def get_task_list(self):
        tasks_url = f"{self.base_url}/external-task?processDefinitionId={self.id_process_definition}"
        async with aiohttp.ClientSession() as session:
            async with session.get(tasks_url) as resp:
                task_list = await resp.json()
                return task_list

    async def get_current_task(self):
        return self.current_task

    async def set_current_task(self):
        task_list = await self.get_task_list()
        current_task = task_list[0]["id"]
        self.current_task = current_task

    async def task_complete(self, approved):
        if not self.current_task:
            await self.set_current_task()
        complete_url = 'http://localhost:8080/engine-rest/engine/default/external-task/' + self.current_task + '/complete'
        req_body = {
            "variables": {
                "approved": {
                    "value": "true",
                    "type": "Boolean"
                }
            },
            "businessKey": "123"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(complete_url, json=req_body):
                await self.set_current_task()
