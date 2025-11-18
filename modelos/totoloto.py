# modelos/totoloto.py
from .loteria_base import LoteriaBase

class Totoloto(LoteriaBase):
    def __init__(self):
        super().__init__("Totoloto", "Número da Sorte")