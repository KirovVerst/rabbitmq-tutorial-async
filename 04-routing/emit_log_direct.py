import asyncio

import aio_pika

EXCHANGE_NAME = "direct_logs"

SEVERITY_INFO = "info"
SEVERITY_WARN = "warning"
SEVERITY_ERROR = "error"
SEVERITIES = (SEVERITY_INFO, SEVERITY_WARN, SEVERITY_ERROR)


async def main():
    conn: aio_pika.Connection = await aio_pika.connect(host="localhost")
    async with conn:
        channel: aio_pika.Channel = await conn.channel()
        exchange = await channel.declare_exchange(
            name=EXCHANGE_NAME,
            type=aio_pika.exchange.ExchangeType.DIRECT
        )
        for severity in SEVERITIES:
            body = f"message with {severity} severity"
            await exchange.publish(message=aio_pika.Message(
                body=body.encode()
            ), routing_key=severity)
            print(f"[x] Sent {severity}: {body}")


if __name__ == '__main__':
    asyncio.run(main())
