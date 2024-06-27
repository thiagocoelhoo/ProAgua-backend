from typing import List

from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, F, Subquery, OuterRef, BooleanField, ExpressionWrapper, Case, When, Value, CharField
from django.db.models.functions import Concat
from ninja import Router, Query
from ninja.pagination import paginate
from ninja.errors import HttpError

from .schemas.sequencia_coletas import *
from .. import models

router = Router(tags=["Sequencias"])


@router.get("/", response=List[SequenciaColetasOut])
@paginate
def list_sequencia(request, filter: FilterSequenciaColetas = Query(...)):
    parametros = models.ParametrosReferencia.objects.first()

    # Consolidar select_related e prefetch_related
    qs = models.SequenciaColetas.objects.select_related(
        'ponto', 'ponto__edificacao', 'ponto__amontante'
    ).prefetch_related(
        'coletas', 'ponto__imagens', 'ponto__associados', 'ponto__edificacao__imagens'
    )

    # Uma única subquery para obter todas as coletas
    coletas = models.Coleta.objects.filter(sequencia=OuterRef('pk')).order_by('data')

    qs = qs.annotate(
        ultima_coleta_turbidez=Subquery(coletas.values('turbidez')[:1]),
        ultima_coleta_cloro=Subquery(coletas.values('cloro_residual_livre')[:1]),
        ultima_coleta_escherichia=Subquery(coletas.values('escherichia')[:1]),
        ultima_coleta_coliformes=Subquery(coletas.values('coliformes_totais')[:1]),
        quantidade_coletas=Count('coletas'),
        status_turbidez=ExpressionWrapper(
            Q(ultima_coleta_turbidez__gte=parametros.min_turbidez) & Q(ultima_coleta_turbidez__lte=parametros.max_turbidez),
            output_field=BooleanField()
        ),
        status_cloro=ExpressionWrapper(
            Q(ultima_coleta_cloro__gte=parametros.min_cloro_residual_livre) & Q(ultima_coleta_cloro__lte=parametros.max_cloro_residual_livre),
            output_field=BooleanField()
        ),
        status=Case(
            When(
                Q(status_turbidez=True) & Q(status_cloro=True) & ~Q(ultima_coleta_escherichia=True) & ~Q(ultima_coleta_coliformes=True),
                then=True
            ),
            output_field=BooleanField()
        ),
        mensagem_turbidez=Case(
            When(
                ultima_coleta_turbidez__gt=parametros.max_turbidez,
                then=Concat(
                    Value("Turbidez está "), 
                    F('ultima_coleta_turbidez') - parametros.max_turbidez,
                    Value(" uT acima do limite máximo")
                )
            ),
            When(
                ultima_coleta_turbidez__lt=parametros.min_turbidez,
                then=Concat(
                    Value("Turbidez está "), 
                    parametros.min_turbidez - F('ultima_coleta_turbidez'),
                    Value(" uT abaixo do limite mínimo")
                )
            ),
            default=Value(""),
            output_field=CharField()
        ),
        mensagem_cloro=Case(
            When(
                ultima_coleta_cloro__gt=parametros.max_cloro_residual_livre,
                then=Concat(
                    Value("Cloro está "), 
                    F('ultima_coleta_cloro') - parametros.max_cloro_residual_livre,
                    Value(" acima do limite máximo")
                )
            ),
            When(
                ultima_coleta_cloro__lt=parametros.min_cloro_residual_livre,
                then=Concat(
                    Value("Cloro está "), 
                    parametros.min_cloro_residual_livre - F('ultima_coleta_cloro'),
                    Value(" abaixo do limite mínimo")
                )
            ),
            default=Value(""),
            output_field=CharField()
        ),
        mensagem_coliformes=Case(
            When(
                ultima_coleta_coliformes=True,
                then=Value("Presença de coliformes")
            ),
            default=Value(""),
            output_field=CharField()
        ),
        mensagem_escherichia=Case(
            When(
                ultima_coleta_escherichia=True,
                then=Value("Presença de escherichia coli")
            ),
            default=Value(""),
            output_field=CharField()
        ),
        status_message=Case(
            When(
                Q(status_turbidez=False) | Q(status_cloro=False) | Q(ultima_coleta_escherichia=True) | Q(ultima_coleta_coliformes=True),
                then=Concat(F('mensagem_turbidez'), Value(". "), F('mensagem_cloro'), Value(". "), F('mensagem_coliformes'), Value(". "), F('mensagem_escherichia'))
            ),
            When(
                Q(quantidade_coletas=0),
                then=Value("Não há coletas registradas para esta sequência.")
            ),
            default=Value("Todos os parâmetros estão dentro dos limites."),
            output_field=CharField()
        )
    )

    if filter.q:
        qs = qs.filter(
            Q(ponto__ambiente__icontains=filter.q) | 
            Q(ponto__edificacao__nome__icontains=filter.q) | 
            Q(ponto__edificacao__codigo__icontains=filter.q)
        )
    
    if filter.ponto__edificacao__campus:
        qs = qs.filter(ponto__edificacao__campus=filter.ponto__edificacao__campus)

    if filter.amostragem:
        qs = qs.filter(amostragem=filter.amostragem)
    
    return filter.filter(qs)


@router.get("/{id_sequencia}", response=SequenciaColetasOut)
def get_sequencia(request, id_sequencia: int):
    qs = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    return qs


@router.post("/")
def create_sequencia(request, payload: SequenciaColetasIn):
    id_ponto = payload.dict().get("ponto")
    ponto = get_object_or_404(models.PontoColeta, id=id_ponto)

    payload_dict = payload.dict()
    payload_dict["ponto"] = ponto

    sequencia = models.SequenciaColetas.objects.create(**payload_dict)
    sequencia.save()
    return {"success": True}


@router.put("/{id_sequencia}")
def update_sequencia(request, id_sequencia: int, payload: SequenciaColetasIn):
    sequencia = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    for attr, value in payload.dict().items():
        setattr(sequencia, attr, value)
    sequencia.save()
    return {"success": True}


@router.delete("/{id_sequencia}")
def delete_sequencia(request, id_sequencia: int):
    sequencia = get_object_or_404(models.SequenciaColetas, id=id_sequencia)
    
    if models.SequenciaColetas.has_dependent_objects(sequencia):
        raise HttpError(409, "Conflict: Related objects exist")

    sequencia.delete()
    return {"success": True}


@router.get("/{id_sequencia}/coletas", response=List[ColetaOut])
def list_coletas_sequencia(request, id_sequencia: int):
    qs = models.Coleta.objects.filter(sequencia__id=id_sequencia)
    return qs
