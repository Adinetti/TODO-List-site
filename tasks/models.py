from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/tag/{}".format(self.slug)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_ending = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} ({}: {})".format(self.title, 
                                    self.user.username, 
                                    self.date_of_creation.isoformat(timespec='seconds'))

    def get_absolute_url(self):
        return "/task/{}".format(self.slug)

