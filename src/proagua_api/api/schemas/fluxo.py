from typing import List 

from .ponto_coleta import PontoColetaOut
from proagua_api.models import PontoColeta, Fluxo
from ninja import Schema, ModelSchema

class FluxoIn(ModelSchema):
    class Config:
        model = Fluxo
        model_fields = ["pontos"]

class FluxoOut(Schema):
    id: int
    pontos: List[PontoColetaOut]
