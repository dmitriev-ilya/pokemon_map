from django.db import models  # noqa F401


class Pokemon (models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(blank=True, null=True)
    description = models.TextField(default='Description not added yet')

    def get_photo_url(self, request):
        photo_url = None
        if self.photo:
            photo_url = request.build_absolute_uri(self.photo.url)
        return photo_url

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} Level {self.level}'
