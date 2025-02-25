from django.db import models
from accounts.models import CustomUser

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('pest_outbreak', 'Pest Outbreak'),
        ('seasonal_tip', 'Seasonal Tip'),
        ('community_update', 'Community Update'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"