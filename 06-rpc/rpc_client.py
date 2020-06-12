import asyncio
from typing import Dict
from typing import Optional
from uuid import uuid4

import aio_pika

QUEUE_NAME = "rpc_queue"


class FibonacciRrpClient:
    def __init__(self, loop):
        self._conn: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None
        self._callback_queue: Optional[aio_pika.Queue] = None
        self._futures: Dict = dict()
        self._loop: asyncio.AbstractEventLoop = loop

    async def connect(self) -> None:
        self._conn: aio_pika.Connection = await aio_pika.connect(host="localhost", loop=self._loop)
        self._channel: aio_pika.Channel = await self._conn.channel()
        self._callback_queue: aio_pika.Queue = await self._channel.declare_queue("", exclusive=True)
        await self._callback_queue.consume(self._on_response)

    async def disconnect(self) -> None:
        await self._conn.close()

    async def _on_response(self, msg: aio_pika.IncomingMessage) -> None:
        future: asyncio.Future = self._futures.pop(msg.correlation_id)
        future.set_result(int(msg.body))

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def call(self, n: int) -> int:
        correlation_id = str(uuid4())
        future = self._loop.create_future()
        self._futures[correlation_id] = future
        await self._channel.default_exchange.publish(
            message=aio_pika.Message(
                body=str(n).encode(),
                reply_to=self._callback_queue,
                correlation_id=correlation_id
            ),
            routing_key=QUEUE_NAME
        )
        return int(await future)


async def main(loop):
    async with FibonacciRrpClient(loop) as client:
        n = 50
        result = await client.call(n)
        print(f"[x] Result for {n} is {result}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
