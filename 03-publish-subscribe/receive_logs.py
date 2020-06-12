import asyncio
import aio_pika


EXCHANGE_NAME = "logs"


async def main(loop: asyncio.AbstractEventLoop):
    print("Logs receiving started")
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost", loop=loop)
    channel: aio_pika.Channel = await conn.channel()
    queue = await channel.declare_queue(name="", exclusive=True)
    await queue.bind(EXCHANGE_NAME)
    await queue.consume(callback_on_message)
    return conn


async def callback_on_message(msg: aio_pika.IncomingMessage) -> None:
    async with msg.process():
        print(f"[x] Received {msg.body.decode()}")
        print("[x] Done")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    connection: aio_pika.Connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
