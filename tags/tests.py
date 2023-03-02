from django.test import TestCase
from django.db.utils import IntegrityError 
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from .models import TaggedItem
from playlists.models import Playlist

# Create your tests here.
class TaggedItemTestCase(TestCase):
    def setUp(self):
        ply_title = "New title"
        self.ply_obj = Playlist.objects.create(title=ply_title)
        self.ply_title = ply_title
        self.ply_obj.tags.add(TaggedItem(tag='new-tag'), bulk=False)
        # self.tag_a = TaggedItem.objects.create(tags='my-new-tag')
        # this above line creates an integrity error so we do the test_content_type_is_not_null below instead

    def test_content_type_is_not_null(self):
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag='my-new-tag')

    def test_create_via_content_type(self):
        # we can create models from content type
        c_type = ContentType.objects.get(app_label='playlists', model='playlist')
        # c_type.model_class(): this will give the same value as from playlists.models import Playlist
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=100, tag='new-tag-2')
        self.assertIsNotNone(tag_a.pk)
        # what happens with generic foreign keys is its not a hard association so
        # it doesn't matter at all if that object exists

    def test_create_via_model_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_app_loader_content_type(self):
        PlaylistKlass = apps.get_model(app_label='playlists', model_name='Playlist')
        c_type = ContentType.objects.get_for_model(PlaylistKlass)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)

    def test_related_field(self):
        self.assertEqual(self.ply_obj.tags.count(), 1)

    def test_related_field_create(self):
        self.ply_obj.tags.create(tag='another-new-tag')
        self.assertEqual(self.ply_obj.tags.count(), 2)

    def test_related_field_query_name(self):
        qs = TaggedItem.objects.filter(playlist__title__iexact=self.ply_title )
        self.assertEqual(qs.count(),1)

    def test_related_field_via_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_qs = TaggedItem.objects.filter(content_type=c_type, object_id=self.ply_obj.id)
        self.assertEqual(tag_qs.count(),1)

    def test_direct_obj_creation(self):
        obj = self.ply_obj
        tag = TaggedItem.objects.create(content_object=obj, tag='another-one')
        self.assertIsNotNone(tag.pk)


    # the difference between:
    # qs = TaggedItem.objects.filter(playlist__title__iexact=self.ply_title ) on test_related_field_query_name
    # and
    # tag_qs = TaggedItem.objects.filter(content_type=c_type, object_id=self.ply_obj.id) on test_related_field_via_content_type
    # first_one: filtering for queryset for the exact title as in ply_title and tags associated to it
    # two playlists if created with same title then it gives error
    # as it looks up all of the playlists with same title
    # second_one: it just looks for number of tags associated to the particular object defined for it
    # not for all of the playlists that has the same title


