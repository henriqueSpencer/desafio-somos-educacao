"""__init__.py
===========================
Este pacote expõe as duas funções principais:
- encontra_expressoes: identifica expressões predefinidas no início de sentenças
- aplica_regras: categoriza textos aplicando regras de inferência
"""

from analizador_de_texto.problema1 import encontra_expressoes
from analizador_de_texto.problema2 import aplica_regras

__all__ = ['encontra_expressoes', 'aplica_regras']