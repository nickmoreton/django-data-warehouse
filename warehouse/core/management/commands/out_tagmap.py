import json

from django.core.management.base import BaseCommand

from warehouse.sitemap.models import Page


class Command(BaseCommand):
    help = "Output tagmap"

    def handle(self, *args, **options):
        pages = Page.objects.all()
        unique_tags = []
        for page in pages:
            tags = page.tag_map.replace("[", "")
            tags = tags.replace("]", "")
            tags = tags.replace("'", "")
            tags = tags.split(",")
            for tag in tags:
                tag = tag.strip()
                if tag not in unique_tags:
                    unique_tags.append(tag)

        tag_dict = {}
        for tag in unique_tags:
            tag_dict[tag] = {
                "block_name": "",
                "field_map": {
                    "title": "",
                    "content": "",
                },
            }

        self.stdout.write(json.dumps(tag_dict, indent=4, sort_keys=True))
