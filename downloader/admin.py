from django.contrib import admin
from .models import Parse


@admin.register(Parse)
class ParseAdmin(admin.ModelAdmin):
    list_display = ("raw_url", "downloadable_url", "created", "times_followed")
