from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('viewer', 'Viewer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='viewer')

    def __str__(self):
        return f"{self.user.username} — {self.role}"

    def is_admin(self):
        return self.role == 'admin'