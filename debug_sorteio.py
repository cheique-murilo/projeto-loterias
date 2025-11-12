import sys
import os
from os.path import abspath, join, dirname

# Adiciona raiz ao path
projeto_root = abspath(join(dirname(__file__), '.'))
sys.path.insert(0, projeto_root)

print("Raiz do projeto:", projeto_root)

try:
    import modelos.sorteio
    print("✅ Módulo 'modelos.sorteio' importado com sucesso.")
    print("Todos os itens no arquivo (dir(modelos.sorteio)):")
    print(dir(modelos.sorteio))
    # Procura por 'Sorteio'
    if 'Sorteio' in dir(modelos.sorteio):
        print("✅ Classe 'Sorteio' encontrada!")
        from modelos.sorteio import Sorteio
        print("Import de Sorteio OK!")
    else:
        print("❌ 'Sorteio' NÃO encontrada. Possíveis culpados:")
        for item in dir(modelos.sorteio):
            if 'sorteio' in item.lower():
                print(f"  - '{item}' (em lowercase ou variável)")
except ImportError as e:
    print(f"❌ Erro ao importar módulo: {e}")
except Exception as e:
    print(f"Erro geral: {e}")