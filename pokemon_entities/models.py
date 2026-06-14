from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name="имя покемона")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="имя покемона(англ)")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="имя покемона(яп)")
    image = models.ImageField(upload_to="pokemon", blank=True, null=True, verbose_name="картинка покемона")
    description = models.TextField(max_length=500, blank=True, verbose_name="описание")
    previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="предыдущая эволюция", related_name="next_evolution")
    

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="ссылка на покемона", related_name="entites")
    lon = models.FloatField(verbose_name="долгота")
    lat = models.FloatField(verbose_name="широта")

    appeared_at = models.DateTimeField(verbose_name="время появленя", blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name="время исчезновения", blank=True, null=True)

    level = models.IntegerField(verbose_name="уровень", blank=True, null=True)
    health = models.IntegerField(verbose_name="хп", blank=True, null=True)
    strenght = models.IntegerField(verbose_name="сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="защита", blank=True, null=True)
    stamina = models.IntegerField(verbose_name="выносливость", blank=True, null=True)

    def __str__(self):
        return self.pokemon.title
