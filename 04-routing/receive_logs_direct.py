import asyncio
import sys
from typing import List

import aio_pika

EXCHANGE_NAME = "direct_logs"
SEVERITY_INFO = "info"


async def main(loop: asyncio.AbstractEventLoop, severities: List[str]) -> aio_pika.Connection:
    print(f"Receiving logs with {', '.join(severities)} severities started")

    conn: aio_pika.Connection = await aio_pika.connect(host="localhost", loop=loop)
    channel = await conn.channel()
    queue = await channel.declare_queue(name="", exclusive=True)

    for severity in severities:
        await queue.bind(EXCHANGE_NAME, severity)
    await queue.consume(callback_on_message)

    return conn


async def callback_on_message(msg: aio_pika.IncomingMessage) -> None:
    async with msg.process():
        print(f"[x] Received {msg.body.decode()}")


if __name__ == '__main__':
    severities = sys.argv[1:] or [SEVERITY_INFO]
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop, severities))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
