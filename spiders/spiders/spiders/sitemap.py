import scrapy
from scrapy.loader import ItemLoader

from ..items import UrlItem


class SitemapSpider(scrapy.Spider):
    name = "sitemap"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:8888"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "spiders.pipelines.SitemapPipeline": 300,
        },
    }

    def parse(self, response):
        pages_container = response.css("ul.wp-block-post-template")

        nav_container = response.css("nav.wp-block-query-pagination")
        next_page = nav_container.css(
            "a.wp-block-query-pagination-next::attr(href)"
        ).get()

        for page in pages_container.css("li"):
            loader = ItemLoader(item=UrlItem())

            if page.css("h2 a::text").get() is None:
                classes = self.get_page_id_from_classlist(page)
                self.logger.info(
                    f"Page ID {classes} No title found for this page. It has not been processed."
                )
                continue

            loader.add_value("wp_id", self.get_page_id_from_classlist(page))
            loader.add_value("title", page.css("h2 a::text").get())
            loader.add_value("url", page.css("h2 a::attr(href)").get())
            yield loader.load_item()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_page_id_from_classlist(self, page):
        """
        Sample class list:
        wp-block-post post-1169 post type-post status-publish format-standard hentry ...

        parse the classes to obtain the number from post-1169
        """
        classes = page.css("li::attr(class)").get().split(" ")

        for class_ in classes:
            if "post-" in class_:
                return class_.replace("post-", "")
