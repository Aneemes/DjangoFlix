from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # CONSTANT = DB_VALUE, USER_DISPLAU_VALUE/VERBOSE_NAME
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN','Unlisted'

    title = models.CharField(
        max_length=225
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    slug = models.SlugField(
        blank=True,
        null=True
    )  
    video_id = models.CharField(
        max_length=225,
        unique=True
    )
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    state = models.CharField(
        max_length=2,
        choices=VideoStateOptions.choices,
        default=VideoStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        # means that the publish_timestamp field will not automatically be set to the current date and time when a new instance of this model is created.
        auto_now_add=False,
        # means that the publish_timestamp field will not automatically be updated to the current date and time every time the model is saved.
        auto_now=False,
        blank=True,
        null=True
    )

    @property
    def is_published(self):
        return self.active

    # The save method is overridden in this model.
    def save(self, *args, **kwargs):
        # If the state attribute of the model instance is set to PUBLISH and the publish_timestamp field does not have a value, the method will set publish_timestamp to the current date
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            # print('save ass timestamp for published')
            self.publish_timestamp = timezone.now()
        # If the state attribute is set to DRAFT, the publish_timestamp field will be set to None
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'


class VideoUnpublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Unpublished Video'
        verbose_name_plural = 'Unpublished Videos'


class VideoActiveProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Active Video'
        verbose_name_plural = 'Active Videos'


class VideoInactiveProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Inactive Video'
        verbose_name_plural = 'Inactive Videos'
