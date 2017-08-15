import hashlib
import foursquare
import requests
from django.conf import settings


class FoursquareBackend(object):
    def __init__(self):
        self.client = foursquare.Foursquare(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            version='20120609')

    def get_venues(self, query, near, section):
        venues = self.client.venues.explore(
            params={
                'query': query,
                'near': near,
                'venuePhotos': True,
                'radius': 30000,
                'section': section

            }
        )['groups'][0]['items']

        coffeeshops = []

        for place in venues:

            venue = place['venue']
            foursquare_id = venue.get("id", '')
            tips = place.get('tips', [])
            categories = venue.get('categories', [])
            address = venue.get('location', {}).get('address', 'Lviv')
            city = venue.get('location', {}).get('city', 'Lviv')
            name = venue.get('name', '')

            hash = hashlib.sha256(''.join((name, address, city)).encode('utf-8')).hexdigest()
            photos = venue.get('photos', {})
            image_url = '{prefix}{size}{suffix}'.format(
                prefix=photos['groups'][0]['items'][0]['prefix'],
                size='width400',
                suffix=photos['groups'][0]['items'][0]['suffix']
            ) if photos and photos['groups'] else ""

            coffeeshop_data = {
                'name': name,
                'city': city,
                'tips': tips[0].get('text', '') if tips else '',
                'tips_url': tips[0].get('canonicalUrl', '') if tips else '',
                'rating': venue.get('rating', 0),
                'url': venue.get('url', ''),
                'phone': venue.get('contact', {}).get('formattedPhone', ''),
                'address': address,
                'category': categories[0].get('name', '') if categories else '',
                'hours': venue.get('hours', {}).get('status', ''),
                'price': venue.get('price', {}).get('message', ''),
                'uid': hash,
                'image_url': image_url,
                'foursquare_id': foursquare_id
            }
            coffeeshops.append(coffeeshop_data)

        return coffeeshops

    def get_venue_avatar(self, foursquare_id):
        avatar_data = self.client.venues(foursquare_id).get('venue', {}).get('page', {}).get('user', {}).get('photo', {})
        if avatar_data:
            avatar_url = "{prefix}{size}{suffix}".format(prefix=avatar_data.get(
                'prefix', ''), suffix=avatar_data.get('suffix'), size='original')
        else:
            avatar_url = ''


        return avatar_url




