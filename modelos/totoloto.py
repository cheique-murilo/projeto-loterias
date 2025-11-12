
from .loteria import Loteria
from .sorteio import Sorteio

class Totoloto(Loteria):
    def __init__(self):
        super().__init__('Totoloto', (1, 49), (1, 13))

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        return len(sorteio.numeros_sorteados) == 5 and all(1 <= n <= 49 for n in sorteio.numeros_sorteados) and len(sorteio.numeros_complementares) == 1 and 1 <= sorteio.numeros_complementares[0] <= 13