from django.db import models
from django.conf import settings

class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        db_index=True
    )
    
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField()

    
    image = models.ImageField(upload_to='notes/images/', null=True, blank=True)
    file = models.FileField(upload_to='notes/files/', null=True, blank=True)


    # For search optimization
    is_deleted = models.BooleanField(default=False, db_index=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_pinned = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_deleted']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title