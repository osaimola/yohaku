from django.db import models
from django.utils import timezone

# Create your models here.
from django.db.models import Model


class Tweet(models.Model):
    tweet_content = models.CharField(max_length=280, blank=False)
    tweet_intro = models.CharField(max_length=31, blank=True)
    publish_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now())
    user_id = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.tweet_content:
            self.tweet_intro = self.tweet_content[:30]
        super(Tweet, self).save(*args, **kwargs)

    def __str__(self):
        return self.tweet_intro


class Identity(models.Model):
    id_count = models.IntegerField(default=1)

    def get_new_id(self):
        self.id_count += 1
        #consider replacing with F function
        return self.id_count - 1

    def __str__(self):
        return str(self.id_count)

