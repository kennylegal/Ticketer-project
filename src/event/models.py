from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class EventModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField(null=False, blank=False)
    venue = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title
