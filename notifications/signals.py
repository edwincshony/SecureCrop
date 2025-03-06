from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from reports.models import PestSighting, TreatmentOutcome
from control_advisory.models import AdvisoryRequest, AdvisoryResponse
from pest_weed_db.models import CropLifecycle
from discussions.models import Thread, Post, Reply
from messaging.models import Message
from accounts.models import CustomUser

# PestSighting Notification
@receiver(post_save, sender=PestSighting)
def notify_pest_sighting(sender, instance, created, **kwargs):
    if created:
        # Notify all agricultural experts
        experts = CustomUser.objects.filter(role='agricultural_expert')
        for expert in experts:
            Notification.objects.create(
                user=expert,
                title=f"New Pest Sighting by {instance.user.username}",
                message=f"A pest sighting has been reported for {instance.crop.name} at {instance.location}.",
                type='pest_outbreak',
                url=f"/expert/pest-sightings/{instance.id}/"
            )

# TreatmentOutcome Notification
@receiver(post_save, sender=TreatmentOutcome)
def notify_treatment_outcome(sender, instance, created, **kwargs):
    if created:
        # Notify the farmer who submitted it and experts
        Notification.objects.create(
            user=instance.user,
            title="Treatment Outcome Recorded",
            message=f"Your treatment for {instance.pest.name} on {instance.crop.name} has been logged.",
            type='community_update',
            url="/farmer/treatment-outcomes/"
        )
        experts = CustomUser.objects.filter(role='agricultural_expert')
        for expert in experts:
            Notification.objects.create(
                user=expert,
                title=f"New Treatment Outcome by {instance.user.username}",
                message=f"Treatment for {instance.pest.name} on {instance.crop.name} reported.",
                type='community_update',
                url="/expert/treatment-outcomes/"
            )

# AdvisoryRequest Notification
@receiver(post_save, sender=AdvisoryRequest)
def notify_advisory_request(sender, instance, created, **kwargs):
    if created:
        # Notify all experts
        experts = CustomUser.objects.filter(role='agricultural_expert')
        for expert in experts:
            Notification.objects.create(
                user=expert,
                title=f"New Advisory Request by {instance.user.username}",
                message=f"Request for {instance.crop_type} regarding {instance.issue_type}.",
                type='community_update',
                url="/expert/advisory-requests/"
            )
    elif instance.status == 'responded' and instance.recommendation:
        # Notify the farmer when responded
        Notification.objects.create(
            user=instance.user,
            title=f"Advisory Response for {instance.crop_type}",
            message=f"An expert has responded to your {instance.issue_type} issue.",
            type='community_update',
            url="/farmer/advisory-responses/"
        )

# CropLifecycle Notification
@receiver(post_save, sender=CropLifecycle)
def notify_crop_lifecycle(sender, instance, created, **kwargs):
    if created:
        # Notify the farmer and experts
        Notification.objects.create(
            user=instance.user,
            title=f"Crop Lifecycle Update: {instance.get_stage_display()}",
            message=f"Updated {instance.crop.name} at {instance.stage}.",
            type='seasonal_tip',
            url="/farmer/crop-lifecycle/"
        )
        experts = CustomUser.objects.filter(role='agricultural_expert')
        for expert in experts:
            Notification.objects.create(
                user=expert,
                title=f"Crop Lifecycle Update by {instance.user.username}",
                message=f"{instance.crop.name} updated to {instance.get_stage_display()}.",
                type='seasonal_tip',
                url="/expert/crop-lifecycle/"
            )

# Thread Notification
@receiver(post_save, sender=Thread)
def notify_thread(sender, instance, created, **kwargs):
    if created:
        # Notify all users except the creator
        users = CustomUser.objects.exclude(id=instance.created_by.id)
        for user in users:
            Notification.objects.create(
                user=user,
                title=f"New Thread: {instance.title}",
                message=f"Started by {instance.created_by.username} in {instance.category.name}.",
                type='community_update',
                url=f"/discussions/thread/{instance.id}/"
            )

# Post Notification
@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        # Notify thread creator if not the poster
        if instance.created_by != instance.thread.created_by:
            Notification.objects.create(
                user=instance.thread.created_by,
                title=f"New Post in {instance.thread.title}",
                message=f"{instance.created_by.username} posted in your thread.",
                type='community_update',
                url=f"/discussions/thread/{instance.thread.id}/"
            )

# Reply Notification
@receiver(post_save, sender=Reply)
def notify_reply(sender, instance, created, **kwargs):
    if created:
        # Notify post creator if not the replier
        if instance.created_by != instance.post.created_by:
            Notification.objects.create(
                user=instance.post.created_by,
                title=f"New Reply to Your Post",
                message=f"{instance.created_by.username} replied in {instance.post.thread.title}.",
                type='community_update',
                url=f"/discussions/thread/{instance.post.thread.id}/"
            )

# Message Notification
@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    if created:
        # Notify all participants except the sender
        for participant in instance.conversation.participants.exclude(id=instance.sender.id):
            Notification.objects.create(
                user=participant,
                title=f"New Message from {instance.sender.username}",
                message="You have a new message in your conversation.",
                type='community_update',
                url=f"/messaging/conversation/{instance.conversation.id}/"
            )