from django.contrib import admin
from .models import Video, VideoAllProxy, VideoPublishedProxy, VideoUnpublishedProxy
# Register your models here.

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id','id', 'is_published']
    search_fields = ['title']
    list_filter = ['active']
    readonly_fields = ['id', 'is_published']
    class Meta:
        model = VideoAllProxy
    # def published(self, obj, *args, **kwargs):
    #     return obj.active

admin.site.register(VideoAllProxy, VideoAllAdmin)

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    # list_filter = ['active']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return Video.objects.filter(active=True)

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)

class VideoUnpublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    # list_filter = ['video_id']
    class Meta:
        model = VideoUnpublishedProxy

    def get_queryset(self, request):
        return Video.objects.filter(active=False)
    
admin.site.register(VideoUnpublishedProxy, VideoUnpublishedProxyAdmin)