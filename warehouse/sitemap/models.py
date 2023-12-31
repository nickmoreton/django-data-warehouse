from django.db import models


class Sitemap(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sitemap"
        verbose_name_plural = "Sitemaps"


class Urls(models.Model):
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    wp_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_scraped_at = models.DateTimeField(null=True, blank=True)
    page_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    tag_map = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"