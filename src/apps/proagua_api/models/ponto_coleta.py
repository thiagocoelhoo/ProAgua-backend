from django.db import models
from .coleta import Coleta
from .image import Image

TIPOS_PONTOS = (
    (1, "Bebedouro"),
    (2, "Reservatório predial superior"),
    (3, "Reservatório predial inferior"),
    (4, "Reservatório de distribuição superior"),
    (5, "Reservatório de distribuição inferior"),
    (6, "CAERN")
)


class PontoColeta(models.Model):
    id = models.AutoField(primary_key=True)
    imagens = models.ManyToManyField(to=Image)
    
    edificacao = models.ForeignKey(
        to="Edificacao",
        related_name="PontoColeta",
        verbose_name="código da edificação",
        on_delete=models.PROTECT,
        blank=False
    )

    ambiente = models.CharField(
        verbose_name="ambiente",
        max_length=255
    )

    tipo = models.IntegerField(
        verbose_name="tipo",
        choices=TIPOS_PONTOS,
        default=(1, "Bebedouro")
    )

    tombo = models.CharField(
        max_length=40,
        verbose_name="tombo",
        blank=True,
        null=True
    )

    amontante = models.ForeignKey(
        to="PontoColeta",
        verbose_name="ponto amontante",
        related_name="ponto_amontante",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    associados = models.ManyToManyField(
        to="PontoColeta",
        verbose_name="reservatorios associados",
        related_name="ponto_associado",
        blank=True,
        null=True
    )

    imagem = models.ImageField(
        upload_to="media/images/edificacoes",
        blank=True,
        null=True
    )

    def status(self) -> bool | None:
        coleta = Coleta.objects.filter(ponto=self).last()
        if coleta:
            return coleta.status

    def status_message(self) -> str | None:
        coleta = Coleta.objects.filter(ponto=self).last()
        if coleta:
            return coleta.status_message


    def has_dependent_objects(instance):
        for related_object in instance._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_manager = getattr(instance, related_name)
            if related_manager.exists():
                return True
        return False

    def __str__(self) -> str:
        return f"Ponto {self.id} - {self.get_tipo_display()}"
