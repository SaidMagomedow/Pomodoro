from dataclasses import dataclass
from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer

    async def open_connection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        await self.open_connection()
        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            await self.close_connection()
