from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
                "detailsUrl": f"static/places/{place.id}.json"
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

    place = get_object_or_404(Place, id=place_id)
    images = Image.objects.filter(place=place)

    image_paths = [image.image.url for image in images]

    location_details = {
        "title": place.title,
        "imgs": image_paths,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "lat": place.lat,
        "lon": place.lon,
    }

    return JsonResponse(location_details, json_dumps_params={'ensure_ascii': False, 'indent': 2})
