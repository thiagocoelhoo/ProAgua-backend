from typing import Optional, ForwardRef

from ninja import Schema, FilterSchema, Field
from django.urls import reverse
from .edficacao import EdificacaoOut
from .image import ImageOut

from ... import models

from typing import List

PontoColetaInRef = ForwardRef('PontoColetaIn')
PontoColetaOutRef = ForwardRef('PontoColetaOut')


class PontoColetaIn(Schema):
    codigo_edificacao: str
    tipo: int
    localizacao: Optional[str] = None
    amontante: Optional[int] = None
    observacao: Optional[str] = None
    tombo: Optional[str] = None
class ReservatorioIn(Schema):
    codigo_edificacao: str
    tipo: int
    quantidade: Optional[int] = None # unico, duplo, triplo
    localizacao: Optional[str] = None
    amontante: Optional[int] = None
    observacao: Optional[str] = None
    capacidade: Optional[int] = None
    material: Optional[str] = None
    fonte_informacao: Optional[str] = None
    

class PontoColetaOut(Schema):
    id: int
    edificacao: EdificacaoOut
    tipo: int
    localizacao: Optional[str] = None
    amontante: Optional[PontoColetaOutRef] = None  # type: ignore
    imagens: List[ImageOut]
    tombo: Optional[str] = None
    quantidade: Optional[int] = None # unico, duplo, triplo
    capacidade: Optional[int] = None
    observacao: Optional[str] = None
    material: Optional[str] = None
    fonte_informacao: Optional[str] = None
    status: Optional[bool] = None
    status_message: Optional[str] = None

    @staticmethod
    def resolve_status_message(obj: models.PontoColeta):
        last = obj.coletas.order_by("data").last()
        if last:
            return last.status_messages
        return "Não há coletas nesse ponto"

class ReservatorioOut(Schema):
    id: int
    edificacao: EdificacaoOut
    tipo: int
    localizacao: str
    amontante: Optional[PontoColetaOutRef] = None  # type: ignore
    imagens: List[ImageOut]
    quantidade: Optional[int] = None
    capacidade: Optional[int] = None
    material: Optional[str] = None
    fonte_informacao: Optional[str] = None
    status: Optional[bool] = None
    status_message: Optional[str] = None

    @staticmethod
    def resolve_status_message(obj: models.PontoColeta):
        last = obj.coletas.order_by("data").last()
        if last:
            return last.status_messages
        return "Não há coletas nesse ponto"

class FilterPontos(FilterSchema):
    q: Optional[str] = Field(
        default=None,
        q=["localizacao__contains", "edificacao__nome__contains"],
        description="Campo de pesquisa por localizacão ou nome de edificação"
    )
    edificacao__campus: Optional[str] = Field(
        default=None,
        alias="campus"
    )
    tipo: List[int] = Field(
        default=[0, 1, 2, 3, 4, 5, 6],
        alias="tipo"
    )
    status: Optional[bool] = Field(default=None)


PontoColetaIn.update_forward_refs()
PontoColetaOut.update_forward_refs()
