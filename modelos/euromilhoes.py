
from .loteria import Loteria
from .sorteio import Sorteio

class Euromilhoes(Loteria):  # Exemplo – mesmo para os outros
    def __init__(self):
        super().__init__('Euromilhoes', (1, 50), (1, 12))

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        return True  # Lê tudo