from datetime import datetime, timedelta
from typing import List
from app.models.notification import Notification
from app.models.user import User
from app.models.book import Book
from app.services.notification_service import NotificationService

class ReminderService:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    async def set_return_reminder(self, user: User, book: Book):
        notification = Notification(
            user_id=user.id,
            message=f"Reminder: Please return the book '{book.title}' within 7 days.",
            created_at=datetime.utcnow(),
            is_read=False
        )
        await self.notification_service.add_notification(notification)

    async def get_reminders(self, user: User) -> List[Notification]:
        return await self.notification_service.get_notifications_by_user_id(user.id)

    async def notify_users(self):
        # Logic to notify users about upcoming return dates
        pass