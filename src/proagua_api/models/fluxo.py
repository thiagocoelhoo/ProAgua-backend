from django.db import models

class Fluxo(models.Model):
    pontos = models.ManyToManyField(to="PontoColeta")
