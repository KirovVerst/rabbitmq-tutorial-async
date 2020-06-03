import asyncio
import aio_pika


async def main():
    conn = await aio_pika.connect(host="localhost")
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        await channel.declare_queue("hello")
        await channel.default_exchange.publish(
            aio_pika.Message(
                body="Hello, World!".encode()
            ),
            routing_key="hello"
        )


if __name__ == '__main__':
    asyncio.run(main())
