from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *
# Register your models here.

# this will actually just function as admin.TabularInline
# there are some caveats:
## if we change content_type and object_id to something diffrent we'll actuall have to
## declare those
## check documentation for django contenttypes
class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0

class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['tag', 'content_type','content_object']
    fields = ['tag', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_type', 'object_id', 'content_object']

    class Meta:
        model = TaggedItem

admin.site.register(TaggedItem, TaggedItemAdmin)