# Generated by Django 5.0 on 2023-12-31 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Page",
                "verbose_name_plural": "Pages",
            },
        ),
        migrations.CreateModel(
            name="Sitemap",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Sitemap",
                "verbose_name_plural": "Sitemaps",
            },
        ),
        migrations.CreateModel(
            name="Urls",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("wp_id", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_scraped_at", models.DateTimeField(blank=True, null=True)),
                ("page_id", models.IntegerField(blank=True, null=True)),
                (
                    "sitemap",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sitemap.sitemap",
                    ),
                ),
            ],
            options={
                "verbose_name": "URL",
                "verbose_name_plural": "URLs",
            },
        ),
    ]