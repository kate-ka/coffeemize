from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from  . models import CoffeePlace, Suggestion


class CoffeePlaceSerializer(serializers.ModelSerializer):

    suggestion = serializers.SerializerMethodField()

    class Meta:

        model = CoffeePlace
        fields = '__all__'

    def get_suggestion(self, obj):
        try:
            # TODO: find how we can get request in serializer
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            return Suggestion.objects.get(coffee_place__id=obj.id, user_id=user).id
        except ObjectDoesNotExist:
            pass



class SuggestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suggestion
        fields = ('visited', 'going', 'show_later', 'never_show', 'id', 'coffee_place')




