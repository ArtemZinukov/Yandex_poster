from django.shortcuts import render
from places.models import Place


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
