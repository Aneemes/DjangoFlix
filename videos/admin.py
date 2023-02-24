from django.contrib import admin
from .models import Video, VideoAllProxy, VideoPublishedProxy, VideoUnpublishedProxy, VideoActiveProxy, VideoInactiveProxy
# Register your models here.


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'id', 'state', 'is_published']
    search_fields = ['title']
    list_filter = ['active', 'state']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']

    class Meta:
        model = VideoAllProxy
    # def published(self, obj, *args, **kwargs):
    #     return obj.active


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    # list_filter = ['active']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return Video.objects.filter(state='PU')


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)


class VideoUnpublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    # list_filter = ['video_id']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']

    class Meta:
        model = VideoUnpublishedProxy

    def get_queryset(self, request):
        return Video.objects.filter(state='DR')


admin.site.register(VideoUnpublishedProxy, VideoUnpublishedProxyAdmin)


class VideoActiveProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'state']
    search_fields = ['title']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']

    class Meta:
        model = VideoActiveProxy

    def get_queryset(self, request):
        return Video.objects.filter(active=True)


admin.site.register(VideoActiveProxy, VideoActiveProxyAdmin)


class VideoInactiveProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'state']
    search_fields = ['title']
    readonly_fields = ['id', 'is_published', 'publish_timestamp']

    class Meta:
        model = VideoInactiveProxy

    def get_queryset(self, request):
        return Video.objects.filter(active=False)


admin.site.register(VideoInactiveProxy, VideoInactiveProxyAdmin)
