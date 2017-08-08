import requests
from django.core.files.base import ContentFile
from django.db import models

from django.conf import settings

from .core.search_backends.foursquare_backend import FoursquareBackend


class CoffeePlace(models.Model):
    name = models.CharField(blank=True, max_length=256)
    city = models.CharField(max_length=256, default='Львів')
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(blank=True, max_length=256)
    hours = models.CharField(blank=True, max_length=256)
    price = models.CharField(blank=True, max_length=256)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    tips = models.TextField(blank=True)
    tips_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='coffee_places', null=True, blank=True)
    category = models.CharField(blank=True, max_length=256)
    uid = models.CharField(max_length=256, unique=True, default='')
    foursquare_id = models.CharField(max_length=256, default='')
    avatar = models.ImageField(upload_to='coffee_places/avatars', null=True, blank=True)

    def get_place_avatar(self):
        if not self.avatar:
            avatar_url = FoursquareBackend().get_venue_avatar(self.foursquare_id)
            if avatar_url:
                avatar = requests.get(avatar_url).content
                self.avatar.save(avatar_url.split('/')[-1], ContentFile(avatar), save=True)
        return self.avatar.url

    def __str__(self):
        return self.name


class Suggestion(models.Model):
    visited = models.NullBooleanField()
    going = models.NullBooleanField()
    show_later = models.NullBooleanField()
    never_show = models.NullBooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="suggestions")
    coffee_place = models.ForeignKey(CoffeePlace, related_name='suggestions')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'coffee_place')

    def __str__(self):
        return '{} suggested to {}'.format(self.coffee_place.name, self.user.username)



