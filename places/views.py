from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from places.models import Place, Image


def show_start_page(request):
    places = Place.objects.all()
    features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lon, place.lat],
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('show_place_detail', args=[place.id])
            }
        }
        features.append(feature)

    context = {
        'places_geo': {
            "type": "FeatureCollection",
            "features": features
        }
    }

    return render(request, 'index.html', context=context)


def show_place_detail(request, place_id):

    place = get_object_or_404(
        Place.objects.select_related('images').prefetch_related('images'),
        id=place_id
    )

    location_details = {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "lat": place.lat,
        "lon": place.lon,
    }

    return JsonResponse(location_details, json_dumps_params={'ensure_ascii': False, 'indent': 2})
