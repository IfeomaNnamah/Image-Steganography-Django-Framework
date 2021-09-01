import django
from django.db import models
from django.utils.safestring import mark_safe
from datetime import datetime
# Create your models here.


class ShareImage(models.Model):
    photo = models.ImageField(models.ImageField(upload_to="media", default='image.jpg'))
    photo_title = models.CharField(max_length=200)
    sender_username = models.CharField(max_length=200)
    recipient_username = models.CharField(max_length=200)
    sent_date = models.DateField()

    def __str__(self):
        return self.photo_title
    # def admin_photo(self):
    #     return mark_safe('<img src="{}" width="120" height="100" />'.format(self.photo.url))
    #
    # admin_photo.short_description = 'Image'
    # admin_photo.allow_tags = True


class verifykey(models.Model):
    photo_title = models.CharField(max_length=200)
    stegokey = models.CharField(max_length=200)
    stegokey_id = models.IntegerField(default=0)

    def __str__(self):
        return self.photo_title