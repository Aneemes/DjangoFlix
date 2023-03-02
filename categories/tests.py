from django.test import TestCase
from playlists.models import Playlist
from .models import Category
# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        cat_a = Category.objects.create(title='Action')
        cat_b = Category.objects.create(title='Comedy',
                                        active=False)
        play_a = Playlist.objects.create(title='Playlist 1', category=cat_a)
        self.cat_a = cat_a
        self.cat_b = cat_b
        self.play_a = play_a

    def test_is_active(self):
        self.assertTrue(self.cat_a.active)

    def test_is_not_active(self):
        self.assertFalse(self.cat_b.active)

    def test_related_playlist(self):
        qs = self.cat_a.playlists.all()
        self.assertEqual(qs.count(),1)
