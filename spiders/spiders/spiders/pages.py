import scrapy
from scrapy.loader import ItemLoader

from warehouse.sitemap.models import SitemapUrl

from ..items import PageItem

objects = SitemapUrl.objects.all()
obj_dict = {}
for entry in objects:
    obj_dict[entry.url] = entry.__dict__


class PagesSpider(scrapy.Spider):
    name = "pages"
    allowed_domains = ["localhost"]
    start_urls = [entry.url for entry in objects]

    custom_settings = {
        "ITEM_PIPELINES": {
            "spiders.pipelines.ScrapePagePipeline": 300,
        },
    }

    def parse(self, response):
        title = response.css("main h1::text").get()
        content = response.css("main div.entry-content").get()

        loader = ItemLoader(item=PageItem())
        loader.add_value("title", title)
        loader.add_value("content", content)
        loader.add_value("wp_id", obj_dict[response.url]["wp_id"])
        yield loader.load_item()
