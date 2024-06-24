from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PontoColeta

# Signal para atualizar os pontos associados
@receiver(m2m_changed, sender=PontoColeta.associados.through)
def update_associados(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            ponto = PontoColeta.objects.get(pk=pk)
            if ponto != instance:  # Se o ponto não for ele mesmo
                for associado in instance.associados.all():
                    if associado != ponto and associado not in ponto.associados.all():  # Modify this line
                        ponto.associados.add(associado)
                if instance not in ponto.associados.all():
                    ponto.associados.add(instance)
    elif action == "post_remove":
        for pk in pk_set:
            ponto = PontoColeta.objects.get(pk=pk)
            if ponto != instance:   # Se o ponto não for ele mesmo
                for associado in instance.associados.all():
                    if associado != ponto and associado in ponto.associados.all():  # Modify this line
                        ponto.associados.remove(associado)
                if instance in ponto.associados.all():
                    ponto.associados.remove(instance)