from worker.celery import send_email_task


class MailClient:

    @staticmethod
    def send_welcome_email(to: str) -> None:
        task_id = send_email_task.delay(f"Welcome email", f"Welcome to pomodoro", to)
        return task_id
