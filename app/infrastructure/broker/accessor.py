import aio_pika

from app.settings import Settings


async def get_broker_connection():
    settings = Settings()
    return await aio_pika.connect_robust(settings.AMQP_URL)
