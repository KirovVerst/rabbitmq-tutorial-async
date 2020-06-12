import asyncio
import sys

import aio_pika

EXCHANGE_NAME = "logs"


async def main(msg: str) -> None:
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost")
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            type=aio_pika.channel.ExchangeType.FANOUT
        )
        await exchange.publish(aio_pika.Message(
            body=msg.encode(),
        ), routing_key="")
    print(f"[x] Sent {msg}")


if __name__ == '__main__':
    message = " ".join(sys.argv[1:]) or "Hello, World!"
    asyncio.run(main(message))
