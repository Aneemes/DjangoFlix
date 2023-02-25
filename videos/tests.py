from django.test import TestCase
from .models import Video, PublishStateOptions
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
# Create your tests here.

class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title='This is my title', video_id='abc')
        self.obj_b = Video.objects.create(title='This is my title', video_id='def',
                             state=PublishStateOptions.PUBLISH)

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)

    def test_valid_title(self):
        title='This is my title'
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        title='This is my title'
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        # can also pass the actul value of state as in db i.e. DR & PU as:
        # qs = Video.objects.filter(state='DR')
        qs = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        qs = Video.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte= now
        )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs =Video.objects.all().published()
        published_qs_2 =Video.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())