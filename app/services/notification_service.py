from datetime import datetime
from typing import List
from app.models.notification import Notification

class NotificationService:
    def __init__(self):
        self.notifications = []

    async def add_notification(self, notification: Notification):
        self.notifications.append(notification)

    async def get_notifications_by_user_id(self, user_id: str) -> List[Notification]:
        return [n for n in self.notifications if n.user_id == user_id]