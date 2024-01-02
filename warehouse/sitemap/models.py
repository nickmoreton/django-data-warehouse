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

    @staticmethod
    def spider_start_urls():
        return [entry.url for entry in SitemapUrl.objects.all()]

    @staticmethod
    def get_wp_ids():
        return {entry.url: entry.wp_id for entry in SitemapUrl.objects.all()}


class PageData(BaseTimestampModel):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    tag_map = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page Data"
        verbose_name_plural = "Pages Data"


def get_signature_choices():
    return (
        # These choice may be generated elsewhere later on
        # they don't really apply to anything specific at the moment.
        ("", ""),
        ("heading_block", "Heading"),
        ("rich_text_block", "Rich Text"),
        ("image_block", "Image"),
        ("gallery_block", "Gallery"),
        ("video_block", "Video"),
        ("audio_block", "Audio"),
        ("quote_block", "Quote"),
        ("code_block", "Code"),
        ("html_block", "HTML"),
        ("markdown_block", "Markdown"),
        ("embed_block", "Embed"),
    )


class Signature(BaseBlockSignature):
    block_name = models.CharField(  # required field for django admin list_display and list_filter
        max_length=255,
        blank=True,
        null=True,
        choices=get_signature_choices(),
    )

    class Meta:
        verbose_name = "Signature"
        verbose_name_plural = "Signatures"
        ordering = ["-signature"]
