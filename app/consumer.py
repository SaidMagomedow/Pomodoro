import json

import aio_pika.abc

from app.infrastructure.broker.accessor import get_broker_connection


async def make_aqmp_consumer():
    connection = await get_broker_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue("callback_mail_queue", durable=True)
    await queue.consume(consume_fail_email)


async def consume_fail_email(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        correlation_id = message.correlation_id
        print(message.body.decode(), correlation_id)