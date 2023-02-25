from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save
# Create your models here.

class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAU_VALUE/VERBOSE_NAME
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN','Unlisted'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
    
class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class Video(models.Model):
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
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        # means that the publish_timestamp field will not automatically be set to the current date and time when a new instance of this model is created.
        auto_now_add=False,
        # means that the publish_timestamp field will not automatically be updated to the current date and time every time the model is saved.
        auto_now=False,
        blank=True,
        null=True
    )
    objects = VideoManager()

    @property
    def is_published(self):
        return self.active

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

pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)
