from django.contrib import admin

from .models import Page, Sitemap, Urls


class UrlsInline(admin.TabularInline):
    model = Urls
    extra = 1


class SitemapAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [UrlsInline]


admin.site.register(Sitemap, SitemapAdmin)


class UrlsAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "wp_id", "last_scraped_at")
    search_fields = ("url", "title", "wp_id")
    list_filter = ("sitemap__name",)


admin.site.register(Urls, UrlsAdmin)


class PageAdmin(admin.ModelAdmin):
    search_fields = ("title",)


admin.site.register(Page, PageAdmin)
