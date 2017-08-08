import requests
from PIL import Image
from io import BytesIO
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from .core.search_backends.foursquare_backend import FoursquareBackend
from .core.suggestion_algorithms.random_algorithm import RandomPlaceAlgorithm

from .models import CoffeePlace, Suggestion
from .serializers import CoffeePlaceSerializer, SuggestionSerializer
from django.core.files.base import ContentFile


User = get_user_model()

def pad_image_to_square(img):
    image = Image.open(BytesIO(img))
    # size = (400, 400)
    # image.thumbnail(size, Image.ANTIALIAS)
    # background = Image.new('RGBA', size, (255, 255, 255, 0))
    # background.paste(
    #     image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
    # )
    # background.save("/Users/kateryna/PycharmProjects/coffeemize/coffee_places/output.bmp")
    longer_side = max(image.size)
    horizontal_padding = (longer_side - image.size[0]) / 2
    vertical_padding = (longer_side - image.size[1]) / 2
    img5 = image.crop(
        (
            -horizontal_padding,
            -vertical_padding,
            image.size[0] + horizontal_padding,
            image.size[1] + vertical_padding
        )
    )
    buffer = BytesIO()
    img5.save(fp=buffer, format='JPEG')
    buff_val = buffer.getvalue()
    return ContentFile(buff_val)


class RandomCoffeePlace(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coffee_places = FoursquareBackend().get_venues(query='сoffee', near='Lviv')
        already_suggested_places = Suggestion.objects.filter(
            coffee_place__uid__in=[item['uid'] for item in coffee_places],
            user=request.user
        )
        coffeeshop_data = RandomPlaceAlgorithm(coffee_places, already_suggested_places).get_random_place()

        image_url = coffeeshop_data.pop('image_url')
        instance, created = CoffeePlace.objects.get_or_create(uid=coffeeshop_data['uid'], defaults=coffeeshop_data)
        instance.get_place_avatar()

        if created and image_url:
            image = pad_image_to_square(requests.get(image_url).content)
            image_name = image_url.split('/')[-1]
            instance.image.save(image_name, image, save=True)


        serializer = CoffeePlaceSerializer(instance, context={'request': request})


        return Response(serializer.data)


class CreateUserSuggestion(CreateAPIView):
    serializer_class = SuggestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateSuggestion(RetrieveUpdateAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)





