import json
from dataclasses import dataclass
from aiokafka import AIOKafkaProducer


@dataclass
class BrokerProducer:
    producer: AIOKafkaProducer
    email_topic: str

    async def open_connection(self) -> None:
        await self.producer.start()

    async def close_connection(self) -> None:
        await self.producer.stop()

    async def send_welcome_email(self, email_data: dict) -> None:
        encode_email_data = json.dumps(email_data).encode()
        await self.open_connection()
        try:
            await self.producer.send(topic=self.email_topic, value=encode_email_data)
        finally:
            await self.close_connection()
