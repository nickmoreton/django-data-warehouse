from django.contrib import admin
from django.utils.safestring import mark_safe


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for all models

    This class provides some common functionality for all models.
    """

    readonly_fields = ("created_at", "updated_at")
    list_display = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.truncated_length = 36  # length to truncate fields

        # list display field manipulation
        first_fields = [
            "name",
            "title",
        ]  # these fields will be displayed first
        last_fields = [  # these fields will be displayed last
            "created_at",
            "updated_at",
            "id",
        ]

        truncated_fields = [
            "content",
            "title",
        ]  # these fields will have content truncated

        remove_fields = []  # these fields will be removed from the list_display

        link_fields = [  # these fields will be displayed as a link to the original wordpress content
            "url",
        ]

        self.list_display = self.get_list_display_fields(
            self.model,
            remove_fields,
            first_fields,
            last_fields,
            truncated_fields,
            link_fields,
        )

        self.search_fields = [  # these fields will be searchable
            field.name
            for field in self.model._meta.fields
            if field.name in first_fields
        ]

    def get_list_display_fields(
        self,
        obj,
        remove_fields,
        first_fields,
        last_fields,
        truncated_fields,
        link_fields,
    ):
        """
        Return the list_display fields for a model

        This method is used to add some common functionality to the admin list_display pages.

        1. add some column ordering
        2. truncate some overly long fields
        3. remove some fields
        4. add some links to open the original content
        """
        fields = sorted([field.name for field in obj._meta.fields])

        for field in first_fields:
            if field in fields:
                fields.remove(field)
                fields.insert(0, field)

        for field in last_fields:
            if field in fields:
                fields.remove(field)
                fields.append(field)

        for field in truncated_fields:
            if field in fields:
                position = fields.index(field)
                fields.insert(position, f"get_truncated_{field}")
                fields.remove(field)

        for field in remove_fields:
            if field in fields:
                fields.remove(field)

        for field in link_fields:
            if field in fields:
                position = fields.index(field)
                fields.insert(position, f"get_link_{field}")
                fields.remove(field)

        return fields

    def get_truncated_content(self, obj):
        return (
            obj.content[: self.truncated_length] + "..."
            if len(obj.content) > self.truncated_length
            else obj.content
        )

    get_truncated_content.short_description = "Content"

    def get_truncated_title(self, obj):
        return (
            obj.title[: self.truncated_length] + "..."
            if len(obj.title) > self.truncated_length
            else obj.title
        )

    get_truncated_title.short_description = "Title"

    def get_link_url(self, obj):
        url = obj.url
        url = f'<a href="{url}" target="_blank">Open</a>'
        return mark_safe(url)

    get_link_url.short_description = "Source Url"
