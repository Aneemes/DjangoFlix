from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    # generic foreign key is very similar to the foreign key we've been using
    # now with this we can pass in a actual object(i.e. category with an id of 1) and can reference that with this tag
    # this is not something stored in db itself but just a way of handeling generic items
    content_object = GenericForeignKey("content_type", "object_id")


    # the following get_related_object does the same work as 
    # the content_object defined as GenericForeignKey above
    # 
    # def get_related_object(self):
    #     Klass = self.content_type.model_class()
    #     return Klass.objects.get(id=self.object_id)