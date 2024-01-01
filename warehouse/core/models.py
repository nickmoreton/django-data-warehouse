from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseBlockSignature(BaseModel):
    signature = models.CharField(max_length=255, unique=True)
    block_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=(
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
        ),
    )

    class Meta:
        abstract = True
