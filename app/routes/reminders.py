from fastapi import APIRouter
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService

router = APIRouter()

notification_service = NotificationService()
reminder_service = ReminderService(notification_service)

@router.get("/{user_id}")
def get_reminders(user_id: int):
    # TODO: fetch notifications for user
    return {"message": f"Reminders for user {user_id}"}

@router.post("/{user_id}/mark-read/{notification_id}")
def mark_read(user_id: int, notification_id: int):
    # TODO: mark notification as read
    return {"message": "Marked as read"}