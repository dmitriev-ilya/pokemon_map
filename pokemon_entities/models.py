from django.db import models  # noqa F401


class Pokemon (models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
