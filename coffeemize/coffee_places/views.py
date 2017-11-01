import requests
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView

from .utils.image import crop_image_to_square
from .core.search_backends.foursquare_backend import FoursquareBackend
from .core.suggestion_algorithms.random_algorithm import RandomPlaceAlgorithm

from .models import CoffeePlace, Suggestion, Visit
from .serializers import CoffeePlaceSerializer, SuggestionSerializer


User = get_user_model()


class RandomCoffeePlace(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        city = request.GET.get('city', 'Lviv')
        coffee_places = FoursquareBackend().get_venues(section='coffee', near=city, query='')

        already_suggested_places = Suggestion.objects.filter(
            coffee_place__uid__in=[item['uid'] for item in coffee_places],
            user=request.user
        )
        coffeeshop_data = RandomPlaceAlgorithm(coffee_places, already_suggested_places).get_random_place()
        if coffeeshop_data:

            image_url = coffeeshop_data.pop('image_url')
            instance, created = CoffeePlace.objects.get_or_create(uid=coffeeshop_data['uid'], defaults=coffeeshop_data)
            instance.get_place_avatar()

            if created and image_url:
                image = crop_image_to_square(requests.get(image_url).content)
                image_name = image_url.split('/')[-1]
                instance.image.save(image_name, image, save=True)

            serializer = CoffeePlaceSerializer(instance, context={'request': request})


            return Response(serializer.data)
        serializer = CoffeePlaceSerializer(None, context={'request': request})
        return Response(serializer.data)



class CreateUserSuggestion(CreateAPIView):
    serializer_class = SuggestionSerializer

    def perform_create(self, serializer):

        suggestion = serializer.save(user=self.request.user)
        if serializer.validated_data.get('going'):
            Visit.objects.create(suggestion=suggestion)



class UpdateSuggestion(RetrieveUpdateAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    def perform_update(self, serializer):

        suggestion = serializer.save(user=self.request.user)
        if serializer.validated_data.get('going'):
            Visit.objects.create(suggestion=suggestion)


class Statistics(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CoffeePlaceSerializer

    def get(self, request, coffee_place):
        instance = CoffeePlace.objects.get(id=coffee_place)
        serializer = CoffeePlaceSerializer(instance=instance, context={'request': request})
        return Response(serializer.data)




