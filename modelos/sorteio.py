# modelos/sorteio.py (Refatorado)

from __future__ import annotations # Usar tipagem futura para clareza
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# 💡 frozen=True impede que as propriedades do sorteio sejam alteradas após a criação
@dataclass(frozen=True)
class Sorteio:
    """Representa um único evento de sorteio de loteria."""

    # Atributos obrigatórios
    data: datetime
    concurso: str
    
    # 💡 Usando list[int] para tipagem moderna (Python 3.9+). Usamos field() para evitar 
    # problemas com default mutável (embora frozen=True resolva isso, é boa prática).
    principais: list[int] = field(default_factory=list)
    complementares: list[int] = field(default_factory=list)
    
    acumulou: bool = False
    jackpot: int = 0
    paises_ganhadores: Optional[str] = ""

    def __post_init__(self):
        """
        Executado após o __init__. Ideal para validação ou ajuste de dados.
        Usamos super().__setattr__ pois a classe é frozen (imutável).
        """
        # 1. Garantir que a lista de números principais esteja SEMPRE ORDENADA.
        # Isso padroniza os dados, mesmo que o Excel os tenha desordenado.
        if self.principais:
            super().__setattr__('principais', sorted(self.principais))
            
        # 2. Garantir que o concurso seja sempre uma string limpa.
        if self.concurso:
            super().__setattr__('concurso', str(self.concurso).strip())

    # 💡 Adicionando um método de representação simples para debug
    def __str__(self) -> str:
        data_str = self.data.strftime("%d/%m/%Y")
        p_str = ', '.join(map(str, self.principais))
        c_str = ', '.join(map(str, self.complementares))
        return f"Sorteio {self.concurso} ({data_str}): P=[{p_str}], C=[{c_str}]"
