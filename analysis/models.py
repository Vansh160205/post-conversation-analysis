# analysis/models.py
from django.db import models

class Conversation(models.Model):
    """Stores a single conversation session."""
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.id or ''} - {self.title or 'Untitled'}"

    def save(self, *args, **kwargs):
        # Save first to get ID, then auto-set title if missing
        super().save(*args, **kwargs)
        if not self.title:
            self.title = f"Chat {self.id}"
            super().save(update_fields=['title'])


class Message(models.Model):
    """Stores a single message within a conversation."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=20)  # "user" or "ai"
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."


class ConversationAnalysis(models.Model):
    """Stores the analysis results for a single conversation."""
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name="analysis")

    # Conversation Quality
    clarity_score = models.FloatField(default=0.0)
    relevance_score = models.FloatField(default=0.0)
    accuracy_score = models.FloatField(default=0.0)
    completeness_score = models.FloatField(default=0.0)

    # Interaction
    sentiment = models.CharField(max_length=20, null=True, blank=True)  # positive, neutral, negative
    empathy_score = models.FloatField(default=0.0)
    response_time_avg = models.FloatField(default=0.0)

    # Resolution
    resolution_rate = models.BooleanField(default=False)
    escalation_need = models.BooleanField(default=False)

    # AI Ops
    fallback_frequency = models.IntegerField(default=0)

    # Overall
    overall_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis for Conversation {self.conversation.id}"
