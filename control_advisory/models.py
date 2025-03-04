from django.db import models
from accounts.models import CustomUser

class AdvisoryRequest(models.Model):
    ISSUE_TYPES = [
        ('pest', 'Pest'),
        ('weed', 'Weed'),
    ]
    STATUS_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='advisory_requests')
    crop_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    recommendation = models.TextField(blank=True, null=True)  # Expert's response
    responded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='advisory_responses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.crop_type} ({self.issue_type}) - {self.status}"
    
class AdvisoryResponse(models.Model):
    advisory_request = models.ForeignKey(AdvisoryRequest, on_delete=models.CASCADE, related_name='responses')
    expert = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='expert_responses')
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.expert.username} on {self.advisory_request.crop_type}"
