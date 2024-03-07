from django.db import models

# Create your models here.
class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class PointSetting(models.Model):
    per_point = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
