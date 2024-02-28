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
    otp = models.CharField(max_length=6, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)

    def send_verification_email(self):
        otp = get_random_string(length=6, allowed_chars='1234567890')
        self.otp = otp
        self.save()
        subject = 'Verify your email address'
        message = f'Your OTP is: {otp}'
        send_mail(subject, message, 'sender@example.com', [self.email])

    def send_approval_notification(self):
        subject = 'Account Approved'
        message = 'Your account has been approved by the admin.'
        send_mail(subject, message, 'sender@example.com', [self.email])

    def send_rejection_notification(self):
        subject = 'Account Rejected'
        message = 'Your account registration has been rejected by the admin.'
        send_mail(subject, message, 'sender@example.com', [self.email])
