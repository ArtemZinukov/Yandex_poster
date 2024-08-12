from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableStackedInline, SortableAdminBase


class ImageInline(SortableStackedInline, admin.TabularInline):
    model = Image
    extra = 1

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Image Preview'

    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag',)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('title',)
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('image_tag', 'image_id', 'place')
    search_fields = ('image_id', 'place')
    list_filter = ('image_id', 'place')
    autocomplete_fields = ('place',)
