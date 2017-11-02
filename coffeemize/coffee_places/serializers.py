from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import CoffeePlace, Suggestion, Visit


class CoffeePlaceSerializer(serializers.ModelSerializer):

    suggestion = serializers.SerializerMethodField()
    visitors_number = serializers.SerializerMethodField()
    said_never = serializers.SerializerMethodField()
    said_never_after_visit = serializers.SerializerMethodField()
    user_visits_count = serializers.SerializerMethodField()

    class Meta:

        model = CoffeePlace
        fields = '__all__'

    def get_suggestion(self, obj):
        try:
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            return Suggestion.objects.get(coffee_place__id=obj.id, user_id=user).id
        except ObjectDoesNotExist:
            pass

    def get_visitors_number(self, obj):
        return obj.suggestions.filter(going=True).count()

    def get_said_never(self, obj):
        return obj.suggestions.filter(never_show=True).count()

    def get_said_never_after_visit(self, obj):
        return obj.suggestions.filter(never_show=True, going=True).count()

    def get_user_visits_count(self, obj):
        try:
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            return Visit.objects.filter(suggestion__user=user, suggestion__coffee_place=obj).count()
        except ObjectDoesNotExist:
            pass


class SuggestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suggestion
        fields = ('going', 'show_later', 'never_show', 'id', 'coffee_place')









