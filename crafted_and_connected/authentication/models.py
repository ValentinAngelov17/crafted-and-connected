from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default_profile_pic.jpg')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    description = models.TextField(default="Без описание", max_length=120)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


