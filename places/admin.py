from django.contrib import admin
from places.models import Place, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'place')
    search_fields = ('image_id', 'place')
    list_filter = ('image_id', 'place')