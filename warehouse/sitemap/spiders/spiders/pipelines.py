import datetime

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from itemadapter import ItemAdapter

from warehouse.sitemap.models import Page, Urls
from warehouse.sitemap.signatures import SignatureBuilder


class ScrapeLogPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        wp_id = adapter["wp_id"]
        url = adapter["url"]
        title = adapter["title"]

        obj, created = Urls.objects.get_or_create(
            wp_id=wp_id, defaults={"url": url, "title": title, "sitemap_id": 1}
        )

        # logging.info(f"Created {wp_id} with {url} and {title} at ID: {obj.id}") if created else logging.info(
        #     f"Updated {wp_id} with {url} and {title} at ID: {obj.id}"
        # )

        return item


class ScrapePagePipeline:
    @sync_to_async
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter["title"]
        content = adapter["content"] or ""

        def get_tag_map(content):
            """
            Get a map of all the tags in the content
            """
            soup = BeautifulSoup(content, "html.parser")
            signature_builder = SignatureBuilder(soup).run()

            return signature_builder.get_unique_signatures

        # Get the ScrapeLogEntry object for updating
        # and finding the BlogPost object ig it exists
        wp_id = adapter["wp_id"]
        log_obj = Urls.objects.filter(wp_id=wp_id).first()

        # May want to only update after a certain amount of time
        # has passed since last scrape
        # or if the page has been updated since last scrape?
        page = Page.objects.create(title=title, content=content)
        content = page.content
        tag_map = get_tag_map(content)
        page.tag_map = tag_map
        page.save()

        log_obj.page_id = page.id
        log_obj.last_scraped_at = datetime.datetime.now()
        log_obj.save()

        return item
