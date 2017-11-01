from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient
from .models import CoffeePlace, Suggestion, Visit


User = get_user_model()


def mocked_decode(*args, **kwargs):
    foo = {
        'sub': 'google-oauth2|117146763105468778683',
        'email': 'katedreamhealer@gmail.com',
        'exp': 9009470234, 'iss': 'https://kateryna-ka.eu.auth0.com/',
        'aud': 'Ypo9Fj5VbH2jGyEI5XvsMu3QNDDE73vR',
        'picture': 'https://lh6.googleusercontent.com/-5WJ-u2z6mTo/AAAAAAAAAAI/AAAAAAAAGP4/yDcBGSNQxzw/photo.jpg',
        'email_verified': True, 'iat': 1509434234
    }

    return foo


class PlaceTestCase(TestCase):
    """
    Tests for RandomCoffeePlace, CreateUserSuggestion, UpdateSuggestion, Statistics views
    """
    client_class = APIClient


    def setUp(self):
        self.user = User.objects.create(username="email@email.com")
        self.venue = CoffeePlace.objects.create(name="Coffee Place", rating=5)

        mock.patch(
            'rest_framework_jwt.utils.jwt_decode_handler',
            new=mocked_decode
        ).start()

    def test_each_random_place_is_saved(self):
        for _ in range(4):
            self.client.get(path='/api-v1/random_coffee_place/',
                            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.")
        venues = CoffeePlace.objects.exclude(name=self.venue.name).count()
        self.assertEqual(venues, 4)

    def test_suggestions_created(self):
        response = self.client.post(path='/api-v1/userplaces/',
                                    data={"show_later": True, "coffee_place": self.venue.id,
                                          "user": self.user.id},
                                    HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.",
                                    )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Visit.objects.all().count(), 0)

    def test_suggestions_created_when_going_true(self):

        response = self.client.post(path='/api-v1/userplaces/',

                                    data={"going": True, "coffee_place": self.venue.id,
                                          "user": self.user.id},
                                    HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.",
                                    )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Visit.objects.all().count(), 1)

    def test_suggestions_updated(self):
        suggestion = Suggestion.objects.create(show_later=True, coffee_place=self.venue, user=self.user)
        response = self.client.patch(path='/api-v1/suggestion/' + str(suggestion.id) + '/',
                                     data={"going": True},
                                     HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.")
        self.assertTrue(response.status_code, HTTP_200_OK)
        self.assertTrue(response.json()["going"])
        self.assertEqual(Visit.objects.filter(suggestion=suggestion).count(), 1)

        # Make one more request. Visits count must be increased every time "going=True" is in request
        response = self.client.patch(path='/api-v1/suggestion/' + str(suggestion.id) + '/',
                                     data={"going": True},
                                     HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.")

        self.assertTrue(response.status_code, HTTP_200_OK)
        self.assertEqual(Visit.objects.filter(suggestion=suggestion).count(), 2)

    def test_coffeeplace_statics_returns_returns_visit_counts_after_update_view(self):

        s = Suggestion.objects.create(going=True, user=self.user, coffee_place=self.venue)
        response = self.client.get(
            path='/api-v1/place/' + str(self.venue.id) + '/statistics/',
            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.",
        )
        self.assertEqual(response.json()['user_visits_count'], 0)
        # check that on update visits are increased
        self.client.patch(
            path='/api-v1/suggestion/' + str(s.id) + '/',
            data={"going": True},
            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
        )
        response = self.client.get(
            path='/api-v1/place/' + str(self.venue.id) + '/statistics/',
            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.",
        )

        self.assertEqual(response.json()['user_visits_count'], 1)
        # check that on update visits are increased
        self.client.patch(
            path='/api-v1/suggestion/' + str(s.id) + '/',
            data={"going": True},
            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
        )
        response = self.client.get(
            path='/api-v1/place/' + str(self.venue.id) + '/statistics/',
            HTTP_AUTHORIZATION="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.",
        )
        self.assertEqual(response.json()['user_visits_count'], 2)


