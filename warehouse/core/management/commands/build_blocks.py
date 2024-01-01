from django.core.management.base import BaseCommand

from warehouse.sitemap.models import Page, Signature


class Command(BaseCommand):
    help = "Build blocks"

    def handle(self, *args, **options):
        pages = Page.objects.all()
        for page in pages:
            tags = page.tag_map.replace("[", "")
            tags = tags.replace("]", "")
            tags = tags.replace("'", "")
            tags = tags.split(",")
            for tag in tags:
                tag = tag.strip()
                obj, created = Signature.objects.get_or_create(signature=tag)
                if created:
                    print("Created signature: {}".format(obj.signature))
                else:
                    print("Signature already exists: {}".format(obj.signature))
