from django.contrib import admin
from . models import CoffeePlace, Suggestion
from accounts.models import User

class SuggestionAdmin(admin.ModelAdmin):
    readonly_fields = ('created','modified')

admin.site.register(CoffeePlace)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(User)
