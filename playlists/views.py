from django.http import Http404
from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import MovieProxy, TVShowProxy, Playlist, TVShowSeasonProxy
from django.utils import timezone
from djangoflix.db.models import PublishStateOptions

class PlaylistMixin():
    template_name = 'playlist_list.html'
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context
    
    def get_queryset(self):
        return super().get_queryset().published()

class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

class MovieDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()

class PlaylistDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()

    # def get_object(self):
    #     request = self.request
    #     kwargs = self.kwargs
    #     print(request, kwargs)
    #     return self.get_queryset().filter(**kwargs).first()
    
class TVShowListView(PlaylistMixin, ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV Shows"

class TVShowDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()

class TVShowSeasonDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            ).published()
            obj = qs.first()
        except:
            raise Http404
        return obj
        # qs = self.get_queryset().filter(parent__slug__iexact=show_slug, 
        # slug__iexact=season_slug)
        # if not qs.count() == 1:
        #     raise Http404
        # return qs.first()

class FeaturedPlaylistListView(PlaylistMixin, ListView):
    # template_name = 'featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = "Featured PLaylists"