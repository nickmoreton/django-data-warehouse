from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True


class BaseTimestampModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseBlockSignature(BaseTimestampModel):
    signature = models.CharField(max_length=255, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, "block_name"):
            # THERE IS PROBABLY A BETTER WAY TO DO THIS

            # You'll likely see this error anyway as the admin will try to
            # use this field as a list_display field and list_filter field.

            # e.g.:
            # block_name = models.CharField(
            #     max_length=255,
            #     blank=True,
            #     null=True,
            #     choices=(
            #         ("", ""),
            #         ("heading_block", "Heading"),
            #         ("rich_text_block", "Rich Text"),
            #         ("image_block", "Image"),
            #         ("gallery_block", "Gallery"),
            #         ("video_block", "Video"),
            #         ("audio_block", "Audio"),
            #         ("quote_block", "Quote"),
            #         ("code_block", "Code"),
            #         ("html_block", "HTML"),
            #         ("markdown_block", "Markdown"),
            #         ("embed_block", "Embed"),
            #     ),
            # )
            raise NotImplementedError(
                "You must define a block_name field on your model"
            )

    class Meta:
        abstract = True
