import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity


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
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        photo_url = pokemon_entity.pokemon.get_photo_url(request)
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            photo_url
        )
    
    pokemons_from_model = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_from_model:
        photo_url = pokemon.get_photo_url(request)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': photo_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
        photo_url = pokemon.get_photo_url(request)
        previous_evolution = pokemon.previous_evolution
        if previous_evolution:
            previous_evolution = {
                "title_ru": previous_evolution.title,
                "pokemon_id": previous_evolution.id,
                "img_url": previous_evolution.get_photo_url(request)
            }
        next_evolution = pokemon.next_evolution.first()
        if next_evolution:
            next_evolution = {
                "title_ru": next_evolution.title,
                "pokemon_id": next_evolution.id,
                "img_url": next_evolution.get_photo_url(request)
            }

        pokemon_metadata = {
            "pokemon_id": pokemon.id,
            "title_ru": pokemon.title,
            "title_en": pokemon.title_en,
            "title_jp": pokemon.title_jp,
            "img_url": photo_url,
            "description": pokemon.description,
            "previous_evolution": previous_evolution,
            "next_evolution": next_evolution
        }
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            photo_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_metadata
    })
