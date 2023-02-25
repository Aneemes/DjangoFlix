from django.db.models.signals import pre_save
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save
from .models import Video

pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)