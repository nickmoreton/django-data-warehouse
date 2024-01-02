# Spiders

First run the app and access the django admin and choose Sitemap and add a new site.

**This needs some more work as the site ID is hardcoded in the SitemapPipeline.**

## How to run

Move to this directory and run the following commands:

### SitemapSpider

```bash
scrapy crawl sitemap
```

### PagesSpider

```bash
scrapy crawl pages
```

After running the spiders, you can check the results in the django admin.

The URLs should be populated and the pages should be created.

## TODO

- [ ] Deal with the hardcoded site ID in the SitemapPipeline
- [ ] Add tests
- [ ] If a page has no title or content there are console warnings.
