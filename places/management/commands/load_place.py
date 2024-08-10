import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
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
            data = response.json()
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Не удалось обработать json'))
            return

        lat = float(data['coordinates']['lat'])
        lon = float(data['coordinates']['lng'])

        place, created = Place.objects.get_or_create(
            title=data['title'],
            defaults={
                'description_short': data['description_short'],
                'description_long': data['description_long'],
                'lat': lat,
                'lon': lon
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Создано новое место: {place.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Место уже существует: {place.title}'))

        for img_url in data['imgs']:
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
