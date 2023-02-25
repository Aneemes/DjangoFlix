from django.db import models


class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAU_VALUE/VERBOSE_NAME
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN','Unlisted'

