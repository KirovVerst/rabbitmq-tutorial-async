import asyncio
from functools import lru_cache

import aio_pika

QUEUE_NAME = "rpc_queue"


async def main(loop):
    print("[x] Awaiting RPC requests")
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost", loop=loop)
    channel: aio_pika.Channel = await conn.channel()
    await channel.set_qos(prefetch_count=1)
    queue: aio_pika.Queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async def callback_on_request(msg: aio_pika.IncomingMessage) -> None:
        return await on_request(msg, exchange=channel.default_exchange)

    await queue.consume(callback_on_request)
    return conn


async def on_request(msg: aio_pika.IncomingMessage, exchange: aio_pika.Exchange) -> None:
    async with msg.process():
        n = int(msg.body)
        print(f"[x] {msg.correlation_id}: calculation for {n} started")
        result = fib(n)
        await exchange.publish(
            aio_pika.Message(
                body=str(result).encode(),
                correlation_id=msg.correlation_id
            ),
            routing_key=msg.reply_to,
        )
        print(f"[x] {msg.correlation_id}: calculation for {n} finished with result {result}")


@lru_cache(maxsize=10)
def fib(n: int) -> int:
    if n < 1:
        return 0
    elif n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
