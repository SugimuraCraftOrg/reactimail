from django.contrib import admin
from .models import MessageTemplate
from .forms import MessageTemplateForm


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    form = MessageTemplateForm
    # model = MessageTemplate
    list_display = (
        "account",
        "title",
        "body_parameters",
        "tags_list",
    )
    ordering = ("account", "title")
    search_fields = ("account", "title")
    filter_horizontal = ("tags",)

    def tags_list(self, obj):
        return obj.tag_names

    tags_list.short_desctipton = "Tags"  # type: ignore
