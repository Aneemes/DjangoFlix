from django.test import TestCase
from .models import Playlist, PublishStateOptions
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
from videos.models import Video
from .models import MovieProxy
# Create your tests here.

class MovieProxyTestCase(TestCase):
    def create_videos(self):
        video_a = Video.objects.create(title='My title', video_id='abc123')
        video_b = Video.objects.create(title='My title b', video_id='abc123b')
        video_c = Video.objects.create(title='My title c', video_id='abc123c')

        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c

        self.video_qs = Video.objects.all()


    def setUp(self):
        self.create_videos()
        self.movie_title = 'This is my title'
        self.movie_a = MovieProxy.objects.create(title=self.movie_title, video=self.video_a)
        movie_b = MovieProxy.objects.create(title='This is my title',
                             state=PublishStateOptions.PUBLISH, video=self.video_a)
        self.published_items_count = 1
        movie_b.videos.set(self.video_qs)
        movie_b.save()
        self.movie_b = movie_b

    def test_movie_clip_items(self):
        count = self.movie_b.videos.all().count()
        self.assertEqual(count, 3)

    def test_movie_video(self):
        self.assertEqual(self.movie_a.video, self.video_a)
        #tests for video in a playlist     

    def test_slug_field(self):
        title = self.movie_title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.movie_a.slug)

    def test_valid_title(self):
        title=self.movie_title
        qs = MovieProxy.objects.filter(title=title)
        self.assertTrue(qs.exists())


    def test_draft_case(self):
        # can also pass the actul value of state as in db i.e. DR & PU as:
        # qs = Playlist.objects.filter(state='DR')
        qs = MovieProxy.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)


    def test_publish_manager(self):
        published_qs =MovieProxy.objects.all().published()
        published_qs_2 =MovieProxy.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())
        self.assertEqual(published_qs.count(), self.published_items_count)