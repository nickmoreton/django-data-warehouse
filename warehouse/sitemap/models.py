from django.db import models

from warehouse.core.models import BaseBlockSignature, BaseTimestampModel


class Sitemap(BaseTimestampModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sitemap"
        verbose_name_plural = "Sitemaps"


class SitemapUrl(BaseTimestampModel):
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    wp_id = models.IntegerField()
    last_scraped_at = models.DateTimeField(null=True, blank=True)
    page_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"


class PageData(BaseTimestampModel):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    tag_map = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page Data"
        verbose_name_plural = "Pages Data"


class Signature(BaseBlockSignature):
    class Meta:
        verbose_name = "Signature"
        verbose_name_plural = "Signatures"
        ordering = ["-signature"]
