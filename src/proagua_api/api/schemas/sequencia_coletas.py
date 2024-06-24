from typing import Optional, List
from datetime import datetime

from ninja import Field, FilterSchema, Schema
from django.urls import reverse

from .coleta import ColetaOut
from .ponto_coleta import PontoColetaOut
from ...models import SequenciaColetas


class SequenciaColetasIn(Schema):
    amostragem: int
    ponto: int


class SequenciaColetasOut(Schema):
    id: int
    amostragem: int
    ponto: PontoColetaOut
    quantidade_coletas: int = None
    coletas_url: str
    status: Optional[bool] = None
    status_message: Optional[str] = None
    ultima_coleta: Optional[datetime] = None

    @staticmethod
    def resolve_coletas_url(obj):
        return reverse("api-1.0.0:list_coletas_sequencia", kwargs={"id_sequencia": obj.id})
    
    @staticmethod
    def resolve_status(obj) -> Optional[bool]:
        last = obj.coletas.last()
        if last:
            return last.analise()["status"]

    @staticmethod
    def resolve_status_message(obj: SequenciaColetas):
        messages = []
        last = obj.coletas.last()
        if last:
            messages.extend(last.analise()["messages"])
            return ', '.join(messages) + "."
        return "Coleta pendente."

    @staticmethod
    def resolve_ultima_coleta(obj: SequenciaColetas):
        last = obj.coletas.order_by("data").last()
        if last:
            return last.data


class FilterSequenciaColetas(FilterSchema):
    q: str = Field(
        default=None,
        q=["ponto__ambiente__contains", "ponto__edificacao__nome__contains", "ponto__edificacao__codigo__contains"],
        description="Campo de pesquisa por ambiente ou nome de edificação"
    )

    amostragem: int = Field(
        default=None,
        alias="amostragem"
    )

    ponto__id: int = Field(
        default=None,
        alias="ponto_id"
    )

    ponto__edificacao__campus: str = Field(
        default=None,
        alias="campus"
    )

    status: bool = Field(
        default=None,
        alias="status"
    )
