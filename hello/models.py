from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import linebreaks


# Create your models here.
from django.utils.safestring import mark_safe


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # for return home after the create of post method
    def get_absolute_url(self):
        # for reverse of return Declare(from django.urls import reverse)
        return reverse('post-detail', kwargs={'pk': self.pk})


