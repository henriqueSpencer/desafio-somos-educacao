"""test_utils.py
============================
Testes unitários para as funções utilitárias do projeto.

Este módulo contém testes para as funções auxiliares encontradas no módulo
utils.py.

Testes implementados:
- test_caminho_amostras: verifica se a função retorna o caminho correto
"""
import os
from analizador_de_texto.utils import caminho_amostras

def test_caminho_amostras():
    """Testa se caminho_amostras usa corretamente os recursos do pacote."""
    # Testa com um arquivo que sabemos que existe
    caminho = caminho_amostras("expressoes.txt")

    # Verifica se o caminho retornado é uma string
    assert isinstance(caminho, str)

    # Verifica se o caminho existe no sistema de arquivos
    assert os.path.exists(caminho)

    # Verifica se o caminho termina com o nome do arquivo
    assert caminho.endswith("expressoes.txt")