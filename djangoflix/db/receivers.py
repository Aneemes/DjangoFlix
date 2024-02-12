from django.utils import timezone
from django.utils.text import slugify
from .models import PublishStateOptions
from .utils import get_unique_slug

def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishStateOptions.PUBLISH
    is_draft = instance.state == PublishStateOptions.DRAFT
    # If the state attribute of the model instance is set to PUBLISH and the publish_timestamp field does not have a value, the method will set publish_timestamp to the current date
    if is_publish and instance.publish_timestamp is None:
        # print('save ass timestamp for published')
        instance.publish_timestamp = timezone.now()
    # If the state attribute is set to DRAFT, the publish_timestamp field will be set to None
    elif is_draft:
        instance.publish_timestamp = None

def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)

def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance, size=5)

