from django.contrib import admin

from warehouse.core.admin import BaseAdmin

from .models import PageData, Signature, Sitemap, SitemapUrl


class UrlsInline(admin.TabularInline):
    model = SitemapUrl
    extra = 1


class SitemapAdmin(BaseAdmin):
    list_display = ("name",)
    inlines = [UrlsInline]


admin.site.register(Sitemap, SitemapAdmin)


class UrlsAdmin(BaseAdmin):
    list_display = ("url", "title", "wp_id", "last_scraped_at", "page_id")
    search_fields = ("url", "title", "wp_id")
    list_filter = ("sitemap__name",)


admin.site.register(SitemapUrl, UrlsAdmin)


class PageAdmin(BaseAdmin):
    search_fields = ("title",)


admin.site.register(PageData, PageAdmin)


class SignatureAdmin(BaseAdmin):
    list_editable = ("block_name",)
    list_display_links = ("signature",)
    list_per_page = 500
    list_filter = ("block_name",)


admin.site.register(Signature, SignatureAdmin)
