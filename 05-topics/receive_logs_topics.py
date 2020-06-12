import asyncio
import sys
from typing import List

import aio_pika

EXCHANGE_NAME = "topic_logs"


async def main(loop: asyncio.AbstractEventLoop, binding_keys: List[str]) -> aio_pika.Connection:
    print(f"Receiving logs with {', '.join(binding_keys)} binding keys started")
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost", loop=loop)
    channel: aio_pika.Channel = await conn.channel()
    queue = await channel.declare_queue(name="", exclusive=True)
    for binding_key in binding_keys:
        await queue.bind(EXCHANGE_NAME, binding_key)
    await queue.consume(callback_on_message)
    return conn


async def callback_on_message(msg: aio_pika.IncomingMessage) -> None:
    async with msg.process():
        print(f"[x] {msg.routing_key}: {msg.body.decode()}")


def get_binding_keys() -> List[str]:
    return sys.argv[1:] if len(sys.argv) > 1 else ["anonymous.info"]


if __name__ == '__main__':
    binding_keys = get_binding_keys()
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop, binding_keys))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
