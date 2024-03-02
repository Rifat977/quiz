from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from course.models import Course

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    def is_email_verification_token_expired(self):
        if self.email_verification_sent_at:
            expiration_time = timezone.timedelta(hours=24)  # 24 hours validity
            return self.email_verification_sent_at + expiration_time < timezone.now()
        return True

