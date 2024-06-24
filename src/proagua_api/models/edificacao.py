from django.db import models
from .image import Image


class Edificacao(models.Model):
    imagens = models.ManyToManyField(to=Image)
    codigo = models.CharField(
        verbose_name="código",
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    nome = models.CharField(
        verbose_name="nome",
        max_length=80)
    campus = models.CharField(
        verbose_name="campus",
        max_length=20,
        choices=(("LE", "Leste"), ("OE", "Oeste")),
        default=(("LE", "Leste"))
    )
    cronograma = models.PositiveIntegerField(
        verbose_name="cronograma",
    )

    def has_dependent_objects(instance):
        for related_object in instance._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_manager = getattr(instance, related_name)
            if related_manager.exists():
                return True
        return False

    def __str__(self) -> str:
        return f"Edificacao {self.codigo}"
