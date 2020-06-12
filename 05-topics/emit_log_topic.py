import asyncio
import sys

import aio_pika

EXCHANGE_NAME = "topic_logs"


async def main(routing_key: str) -> None:
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost")
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        exchange = await channel.declare_exchange(
            name=EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC
        )
        message = f"message with {routing_key}"
        await exchange.publish(
            aio_pika.Message(
                body=message.encode()
            ),
            routing_key=routing_key
        )
        print(f"[x] Sent {routing_key}: {message}")


def get_routing_key() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else "anonymous.info"


if __name__ == '__main__':
    routing_key = get_routing_key()
    asyncio.run(main(routing_key))
