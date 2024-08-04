import uuid
from dataclasses import dataclass


from app.broker.producer import BrokerProducer

from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcome_email(self, to: str) -> None:
        email_body = {
            "message": "Welcome to pomodoro",
            "user_email": to,
            "subject": "Welcome message",
            "correlation_id": str(uuid.uuid4()),
        }
        await self.broker_producer.send_welcome_email(email_data=email_body)

        return
