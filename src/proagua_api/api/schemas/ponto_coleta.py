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
    ambiente: str
    tombo: Optional[str] = None
    tipo: int
    amontante: Optional[int] = None
    associados: Optional[List[int]] = None


class PontoColetaOut(Schema):
    id: int
    imagens: List[ImageOut]
    ambiente: str
    tipo: int
    tombo: Optional[str] = None
    edificacao: EdificacaoOut
    edificacao_url: str
    fluxos_url: str
    status: Optional[bool] = None
    status_message: Optional[str] = None
    amontante: Optional[PontoColetaOutRef] = None # type: ignore
    associados: Optional[List[int]] = None # type: ignore

    @staticmethod
    def resolve_associados(self):
        return [ponto.id for ponto in self.associados.all()]

    @staticmethod
    def resolve_edificacao_url(self):
        return reverse("api-1.0.0:get_edificacao", kwargs={"cod_edificacao": self.edificacao.codigo})

    @staticmethod
    def resolve_fluxos_url(self):
        return reverse("api-1.0.0:get_fluxos", kwargs={"id_ponto": self.id})
    
    @staticmethod
    def resolve_status_message(obj: models.PontoColeta):
        messages = []
        last = obj.coletas.order_by("data").last()
        
        if last:
            messages.extend(last.analise()["messages"])

        if len(messages) > 0:
            return ', '.join(messages) + "."
        
        return "Não há coletas nesse ponto"


class FilterPontos(FilterSchema):
    q: Optional[str] = Field(
        default=None,
        q=["ambiente__contains", "edificacao__nome__contains"],
        description="Campo de pesquisa por ambiente ou nome de edificação"
    )
    edificacao__campus: Optional[str] = Field(
        default=None,
        alias="campus"
    )
    tipo: List[int] = Field(
        default=[1, 2, 3, 4, 5, 6],
        alias="tipo"
    )
    fluxos: Optional[int] = None
    status: Optional[bool] = Field(default=None)

PontoColetaIn.update_forward_refs()
PontoColetaOut.update_forward_refs()