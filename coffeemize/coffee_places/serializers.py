from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from  . models import CoffeePlace, Suggestion


class CoffeePlaceSerializer(serializers.ModelSerializer):

    suggestion = serializers.SerializerMethodField()
    first_visit = serializers.SerializerMethodField()
    visitors_number = serializers.SerializerMethodField()
    said_never = serializers.SerializerMethodField()

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

    def get_first_visit(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        suggestion = Suggestion.objects.filter(user=user, coffee_place=obj, visited__isnull=True)
        return suggestion.count() > 0

    def get_visitors_number(self, obj):
        return obj.suggestions.filter(visited=True).count()

    def get_said_never(self, obj):
        return obj.suggestions.filter(never_show=True).count()



class SuggestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suggestion
        fields = ('visited', 'going', 'show_later', 'never_show', 'id', 'coffee_place')









