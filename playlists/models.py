from django.db import models
from videos.models import *
from categories.models import *
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, unique_slugify_pre_save
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem
from ratings.models import Rating
from django.db.models import Avg, Max, Min
# Create your models here.

class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAU_VALUE/VERBOSE_NAME
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN','Unlisted'

# model manager and  queryset are made to reduce redundant and get querysets for filtering

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
    
class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def featured_playlists(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "TVS", "TV Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLY", "Playlist"

    # refrencing itself as "self" instead of a model name
    # this is for making playlist of playlist such as a show(i.e. parent playlist)
    # can have multiple seasons(i.e. child playlist or playlist itself)
    # this same concepts can be used in treading of comments like a comment can be a parent comment and the sub comments under it are its child comments
    # also again the sub comment can have multiple of its own sub comment which can all be threaded together with this concept
    parent = models.ForeignKey("self",blank =True,  null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, related_name='playlists', on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(
        max_length=225
    )
    type = models.CharField(
        max_length=3, 
        choices=PlaylistTypeChoices.choices, 
        default=PlaylistTypeChoices.PLAYLIST
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    slug = models.SlugField(
        blank=True,
        null=True
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        related_name = "playlist_featured",
        null=True,
        blank=True
    ) #this gives one video per playlist
    videos = models.ManyToManyField(Video, blank=True, related_name="playlist_item", 
                                    through="PlaylistItem")
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
    # for creating a reverse relation of the GenericForeignKey
    # this too isnt adding anything to the database as a new field 
    # but just giving us some convienence method to use it for the lookups between datatable
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    ratings = GenericRelation(Rating, related_query_name='playlist')

    objects = PlaylistManager()

    # with the def str below the season table shows parent playlists title
    # instead of as before where it only said Playlist object(<pk>)
    def __str__(self):
        return self.title
    
    # doing this aggregation calls every time will be computationally expensive
    # so making a signal to do it for us and storing it as a rating_avg as FK on playlist
    # will be applicable
    def get_rating_avg(self):
        return Playlist.objects.filter(id=self.id).aggregate(Avg("ratings__value"))
    
    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(max=Max("ratings__value"), min=Min("ratings__value"))

    def get_short_display(self):
        return ""

    @property
    def is_published(self):
        return self.active

class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW)

class TVShowProxy(Playlist):
    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args,**kwargs)

    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON)
    
class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonProxyManager()

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args,**kwargs)

class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)
    
class MovieProxy(Playlist):
    objects = MovieProxyManager()

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    # to overwrite the save method to save a playlist as a movie when added from movie proxy
    # otherwisse the default type would be PLAYLIST 
    # this is also done for the seasons and tv show proxy so when adding it would not default to
    # being a playlist itself
    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args,**kwargs)


class PlaylistItem(models.Model):
    # now with this what we can do is:
    # playlist_obj.playlistitem_set.all()
    # basically it's just as using a ManyToMany Field as(    # videos = models.ManyToManyField(Video, blank=True, related_name="playlist_item"))
    # but itll now be a playlist queryset and not video queryset
    # i.e. PlaylistItem.objects.all()
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']
        
    #with the oder field added we can do:
    # qs = PlaylistItem.objects.filter(playlist=my_playlist_obj).order_by('order')


pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(unique_slugify_pre_save, sender=Playlist)

pre_save.connect(publish_state_pre_save, sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowProxy)

pre_save.connect(publish_state_pre_save, sender=TVShowSeasonProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowSeasonProxy)

pre_save.connect(publish_state_pre_save, sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save, sender=MovieProxy)