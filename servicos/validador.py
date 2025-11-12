
import sys
from os.path import join, dirname, abspath
from typing import Dict

# Adiciona raiz ao path
projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.loteria import Loteria

class Validador:
    @staticmethod
    def validar_loterias(loterias: Dict[str, Loteria]) -> bool:
        for nome, loteria in loterias.items():
            for sorteio in loteria.sorteios:
                if not loteria.validar_sorteio(sorteio):
                    print(f"Erro de validação em {nome}: {sorteio}")
                    return False
        print("Todos os dados validados com sucesso!")
        return True