import datetime
from datetime import timedelta
import random

from django.utils import timezone


class RandomPlaceAlgorithm(object):
    """
    algorithm finds the list of earlier suggested places, a user wouldn't visit,
   excludes from the foursquare list these places and
     gets a random coffee place from the prepared list

    """

    def __init__(self, places, already_suggested_places):
        self.places = places
        self.already_suggested_places = already_suggested_places

    def _get_banned_places(self):
        """

        :return:
        a list of places the user is not interested in

        """
        banned_places_uids = []

        if self.already_suggested_places.exists():
            d_today = datetime.date.today()

            for suggestion in self.already_suggested_places:
                if suggestion.never_show:
                    banned_places_uids.append(suggestion.coffee_place.uid)

                if suggestion.visits.all():
                    today = timezone.now()
                    visited_date = suggestion.visits.latest("visit_date").visit_date
                    if today - visited_date < timedelta(7):
                        banned_places_uids.append(suggestion.coffee_place.uid)

                elif suggestion.show_later:
                    if suggestion.modified.date() == d_today:
                        banned_places_uids.append(suggestion.coffee_place.uid)

            return banned_places_uids
        else:
            return []

    def get_random_place(self):
        """
        :return:
        a coffee place, randomly selected from prepared list

        """
        coffeeplaces = [place for place in self.places if place['uid'] not in self._get_banned_places()]
        random_coffeshop_data = random.choice(coffeeplaces) if coffeeplaces else None
        return random_coffeshop_data



