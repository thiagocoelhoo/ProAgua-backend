from typing import List

from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from ninja import Router, Query
from ninja.pagination import paginate
from ninja.errors import HttpError

from .schemas.sequencia_coletas import *
from .. import models

router = Router(tags=["Sequencias"])


@router.get("/", response=List[SequenciaColetasOut])
@paginate
def list_sequencia(request, filter: FilterSequenciaColetas = Query(...)):
    qs = models.SequenciaColetas.objects.select_related('ponto', 'ponto__edificacao', 'ponto__amontante')
    qs = qs.prefetch_related('ponto__imagens', 'ponto__associados', 'ponto__edificacao__imagens')
    qs = qs.annotate(quantidade_coletas=Count('coletas'))

    if filter.q:
        qs = qs.filter(
            Q(ponto__ambiente__contains=filter.q) | Q(ponto__edificacao__nome__contains=filter.q) | 
            Q(ponto__edificacao__codigo__contains=filter.q)
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
