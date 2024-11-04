from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = (
        "account",
        "name",
    )
    ordering = ("account", "name")
    search_fields = ("account", "name")
