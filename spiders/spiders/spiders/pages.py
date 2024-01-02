import scrapy
from scrapy.loader import ItemLoader

from warehouse.sitemap.models import SitemapUrl

from ..items import PageItem


class PagesSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)
        self.wp_ids_lookup = SitemapUrl.get_wp_ids()

    name = "pages"
    allowed_domains = ["localhost"]
    start_urls = SitemapUrl.spider_start_urls()

    custom_settings = {
        "ITEM_PIPELINES": {
            "spiders.pipelines.PagesPipeline": 300,
        },
    }

    def parse(self, response):
        title = response.css("main h1::text").get()
        content = response.css("main div.entry-content").get()

        loader = ItemLoader(item=PageItem())
        loader.add_value("title", title)
        loader.add_value("content", content)
        loader.add_value("wp_id", self.wp_ids_lookup[response.url])
        yield loader.load_item()
