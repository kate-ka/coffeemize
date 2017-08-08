from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
from coffee_places.models import CoffeePlace, Suggestion
from django.conf import settings


User = get_user_model()



# Create your tests here.


class PlaceTestCase(TestCase):
    """
    Tests for RandomCoffeePlace view
    """
    client_class = APIClient

    def test_save_random_places(self):
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        venues = CoffeePlace.objects.all().count()
        self.assertEqual(venues, 3)

    def test_suggestions_create(self):
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.get(path='/api-v1/random_coffee_place/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        venues = CoffeePlace.objects.all()
        user = User.objects.create(username="kateryna")
        response = self.client.post(path='/api-v1/userplaces/', data={"visited":"true", "going":"false", "later":"false", "never": "false", "user":user, "coffee_place": venues[0]}, content_type='application/json')

        # Suggestion.objects.create(visited=True, going=False, later=False, never=False, user=user, coffee_place=venues[0])
        # Suggestion.objects.create(visited=False, going=False, later=False, never=False, user=user, coffee_place=venues[1])
        # Suggestion.objects.create(visited=False, going=False, later=True, never=False, user=user, coffee_place=venues[2])
        #







