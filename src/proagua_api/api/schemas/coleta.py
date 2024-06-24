from typing import List, Optional
from datetime import date, datetime

from ninja import Schema, FilterSchema, Field
from django.urls import reverse

from ... import models
from .ponto_coleta import PontoColetaOut

class ColetaIn(Schema):
    sequencia_id: int
    ponto_id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    data: datetime
    responsavel: List[int]
    ordem: str


class ColetaOut(Schema):
    id: int
    temperatura: float
    cloro_residual_livre: float
    turbidez: float
    coliformes_totais: bool
    escherichia: bool
    cor: float
    data: datetime
    responsaveis_id: List[int]
    responsaveis_url: str
    ordem: str
    links: dict = {}
    sequencia_url: str
    sequencia_id: int
    ponto_url: str
    ponto: PontoColetaOut
    status: Optional[bool] = None
    status_messages: Optional[List[str]] = None

    @staticmethod
    def resolve_responsaveis_id(obj: models.Coleta):
        return [r.id for r in obj.responsavel.all()]

    @staticmethod
    def resolve_responsaveis_url(obj):
        return reverse("api-1.0.0:get_responsaveis_coleta", kwargs={"id_coleta": obj.id})

    @staticmethod
    def resolve_sequencia_url(obj):
        return reverse("api-1.0.0:get_sequencia", kwargs={"id_sequencia": obj.sequencia.id})

    @staticmethod
    def resolve_ponto_url(obj):
        return reverse("api-1.0.0:get_ponto", kwargs={"id_ponto": obj.ponto.id})

    @staticmethod
    def resolve_links(obj: models.Coleta):
        return {
            "sequencia": {
                "id_sequencia": obj.sequencia.id,
                "url_sequencia": reverse("api-1.0.0:get_sequencia", kwargs={"id_sequencia":obj.sequencia.id}),
            }
            ,"ponto_coleta": {
                "id_ponto": obj.ponto.id,
                "url_ponto": reverse("api-1.0.0:get_ponto", kwargs={"id_ponto":obj.ponto.id}),
             }
        }

    @staticmethod
    def resolve_status_messages(obj: models.Coleta):
        return obj.analise()["messages"]


class FilterColeta(FilterSchema):
    responsavel__username__contains: str = Field(
        default=None,
        q=["responsavel__username__contains"]
    )
    
    data__gte: date = Field(
        default=None,
        alias="data_minima"
    )
    
    data__lte: date = Field(
        default=None,
        alias="data_maxima"
    )
    
    sequencia_id: int = Field(
        default=None,
        alias="sequencia__id"
    )
    
    temperatura__gte: float = Field(
        default=None,
        alias="temperatura_minima"
    )
    
    temperatura__lte: float = Field(
        default=None,
        alias="temperatura_maxima"
    )
    
    cloro_residual_livre__gte: float = Field(
        default=None,
        alias="cloro_residual_livre_minimo"
    )
    
    cloro_residual_livre__lte: float = Field(
        default=None,
        alias="cloro_residual_livre_maximo"
    )
    
    turbidez__gte: float = Field(
        default=None,
        alias="turbidez_minima"
    )
    
    turbidez__lte: float = Field(
        default=None,
        alias="turbidez_maxima"
    )
    
    coliformes_totais: bool = Field(
        default=None,
        alias="coliformes_totais"
    )
    
    escherichia: bool = Field(
        default=None,
        alias="escherichia"
    )
    
    cor__gte: float = Field(
        default=None,
        alias="cor_minima"
    )
    
    cor__lte: float = Field(
        default=None,
        alias="cor_maxima"
    )
    
    ordem: str = Field(
        default=None,
        alias="ordem"
    )

    ponto__edificacao__codigo__exact: str = Field(
        default=None,
        alias="codigo_edificacao"
    )
    
    ponto__id: Optional[int] = Field(
        default=None,
        alias="ponto_id"
    )