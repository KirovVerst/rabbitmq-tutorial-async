import asyncio

import aio_pika


async def main(loop):
    conn = await aio_pika.connect(host="localhost", loop=loop)
    channel: aio_pika.Channel = await conn.channel()
    queue = await channel.declare_queue("hello")
    await queue.consume(callback_on_message, no_ack=False)
    return conn


async def callback_on_message(msg: aio_pika.IncomingMessage):
    async with msg.process():
        print(f"[x] Received {msg.body.decode()}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
