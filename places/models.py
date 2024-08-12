from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название места')
    short_description = models.TextField(blank=True, verbose_name="Краткое описание")
    long_description = HTMLField(blank=True, verbose_name="Полное описание")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        verbose_name='Название локации',
        related_name='images'
    )
    image = models.ImageField(upload_to='images/', verbose_name="Картинка")
    image_id = models.PositiveIntegerField(db_index=True, default=0, verbose_name='Номер картинки')

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"
        ordering = ['image_id']

    def __str__(self):
        return str(self.place)

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', self.image.url)
        return "No Image"

    image_tag.short_description = 'Предпросмотр изображения'
