import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Размещение данных из json в БД'

    def add_arguments(self, parser):
        parser.add_argument('load_place', type=str, help='Напишите URL адрес json файла')

    def handle(self, *args, **kwargs):
        json_url = kwargs['load_place']

        try:
            response = requests.get(json_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка HTTP: {http_err}'))
            return
        except Exception as err:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {err}'))
            return

        try:
            payload = response.json()
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Не удалось обработать json'))
            return

        lat = payload['coordinates']['lat']
        lon = payload['coordinates']['lng']
        try:
            place, created = Place.objects.get_or_create(
                title=payload['title'],
                defaults={
                    'description_short': payload['description_short'],
                    'description_long': payload['description_long'],
                    'lat': lat,
                    'lon': lon
                }
            )
        except MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR(f'Ошибка: найдено несколько мест с названием "{payload["title"]}".'))
            return

        if created:
            self.stdout.write(self.style.SUCCESS(f'Создано новое место: {place.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Место уже существует: {place.title}'))

        for img_url in payload['imgs']:
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                file_name = img_url.split("/")[-1]

                image = Image(place=place)
                image.image.save(file_name, ContentFile(img_response.content), save=True)
                self.stdout.write(self.style.SUCCESS(f'Изображение загружено и сохранено: {file_name}'))
            except requests.exceptions.HTTPError as http_err:
                self.stdout.write(self.style.ERROR(f'Не удалось загрузить изображение с URL: {img_url} - {http_err}'))
            except Exception as err:
                self.stdout.write(self.style.ERROR(f'Произошла ошибка при загрузке изображения: {err}'))

        self.stdout.write(self.style.SUCCESS('Импорт данных завершен!'))
