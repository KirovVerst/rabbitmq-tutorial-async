import asyncio
import aio_pika
import time

QUEUE_NAME = 'task_queue'


async def main(loop):
    conn = await aio_pika.connect(host='localhost', loop=loop)
    channel: aio_pika.Channel = await conn.channel()
    await channel.set_qos(prefetch_count=1)
    queue: aio_pika.Queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(callback_on_message)
    return conn


async def callback_on_message(msg: aio_pika.IncomingMessage):
    with msg.process():
        print(f'[x] Received {msg.body.decode()}')
        time.sleep(msg.body.count(b'.'))
        print('[x] Done')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
