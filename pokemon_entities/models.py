from django.db import models  # noqa F401


DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


class Pokemon(models.Model):
    title = models.CharField('Название на русском',max_length=200)
    title_en = models.CharField('Название на английском', max_length=200, default='')
    title_jp = models.CharField('Название на японском', max_length=200, default='')
    photo = models.ImageField('Изображение', blank=True, null=True)
    description = models.TextField('Описание', default='Description not added yet')
    previous_evolution = models.ForeignKey(
        "self",
        verbose_name='Предыдущая стадия',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolution'
    )

    def get_photo_url(self, request):
        photo_url = DEFAULT_IMAGE_URL
        if self.photo:
            photo_url = request.build_absolute_uri(self.photo.url)
        return photo_url

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE,
        related_name='entities'
    )
    appeared_at = models.DateTimeField('Появляется', null=True, blank=True)
    disappeared_at = models.DateTimeField('Исчезает', null=True, blank=True)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} Level {self.level}'
