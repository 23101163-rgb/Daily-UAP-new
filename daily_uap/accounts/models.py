from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
    ]

    PROFESSION_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES, default='student')  # ✅ added
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
