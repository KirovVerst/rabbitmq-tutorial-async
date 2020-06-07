import asyncio
import sys
import aio_pika

ROUTING_KEY = 'task_queue'
QUEUE_NAME = 'task_queue'


async def main(msg: str) -> None:
    conn = await aio_pika.connect(host='localhost')
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        await channel.declare_queue(QUEUE_NAME, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=msg.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=ROUTING_KEY,
        )
    print(f'[x] Sent {msg}')


if __name__ == '__main__':
    message = ' '.join(sys.argv[1:]) or 'Hello, World!'
    asyncio.run(main(message))
