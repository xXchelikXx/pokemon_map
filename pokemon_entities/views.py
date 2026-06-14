import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime

from django.http import Http404

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    today_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=today_time, disappeared_at__gt=today_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        raise Http404("Покемон не найден")

    today_time = localtime()
    pokemon = {
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'title_ru': requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        'description': requested_pokemon.description
    }
    prev_evolution = requested_pokemon.previous_evolution
    if prev_evolution:
        pokemon['previous_evolution'] = {
            'pokemon_id': prev_evolution.id,
            'img_url': request.build_absolute_uri(prev_evolution.image.url),
            'title_ru': prev_evolution.title,
        }
    next_evolution = requested_pokemon.next_evolutions.first()
    if next_evolution:
        pokemon['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url),
            'title_ru': next_evolution.title,
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.entities.filter(appeared_at__lt=today_time, disappeared_at__gt=today_time):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
        

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
