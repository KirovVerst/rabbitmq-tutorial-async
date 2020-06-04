import asyncio
import sys
import aio_pika


async def main(msg: str) -> None:
    conn = await aio_pika.connect(host='localhost')
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        await channel.declare_queue('hello')
        await channel.default_exchange.publish(
            aio_pika.Message(body=msg.encode()),
            routing_key='hello'
        )
    print(f'[x] Sent {msg}')


if __name__ == '__main__':
    message = ' '.join(sys.argv[1:]) or 'Hello, World!'
    asyncio.run(main(message))
