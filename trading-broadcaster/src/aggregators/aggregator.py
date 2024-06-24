import asyncio

from websockets import ConnectionClosed
from websockets.client import connect
from concurrent.futures import ProcessPoolExecutor

task_executer = ProcessPoolExecutor(max_workers=3)

class Aggregator:
    url: str
    connection: any
    providers_count: int
    task: any

    def __init__(self, url):
        self.url = url
        self.listener = None
        self.sender = None
        self.providers_count = 0
        
    def inc_providers_count(self):
        self.providers_count += 1

    def clear_providers_count(self):
        self.providers_count = 0
    
    async def start_listening_aggregator(self):
        self.listener = await connect(self.url)
        self.sender = await connect(self.url)
        self.task = asyncio.create_task(self.__listen_to_aggregator(), name=self.url)

    async def stop_listening_aggregator(self):
        await self.listener.close()
        await self.sender.close()
        
    async def __listen_to_aggregator(self):
        try:
            while self.listener.open:
                data = await self.listener.recv()
                print(data)
        except ConnectionClosed:
            await self.stop_listening_aggregator()
            

