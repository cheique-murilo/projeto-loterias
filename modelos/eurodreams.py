
from .loteria import Loteria
from .sorteio import Sorteio

class Eurodreams(Loteria):  # Exemplo – mesmo para os outros
    def __init__(self):
        super().__init__('Eurodreams', (1, 40), (1, 5))

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        return True  # Lê tudo