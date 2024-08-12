from django.db import models
from django.utils.html import mark_safe
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название места')
    short_description = models.TextField(blank=True, verbose_name="краткое описание")
    long_description = HTMLField(blank=True, verbose_name="полное описание")
    lat = models.FloatField(verbose_name="широта")
    lon = models.FloatField(verbose_name="долгота")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Название локации', related_name='images')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="картинка")
    image_id = models.PositiveIntegerField(db_index=True, default=0, verbose_name='номер картинки')

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="width: 200px; height: 200px;" />')
        return "No Image"

    image_tag.short_description = 'Image Preview'

    def __str__(self):
        return str(self.place)

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"
        ordering = ['image_id']
