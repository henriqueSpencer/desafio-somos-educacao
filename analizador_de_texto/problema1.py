"""problema1.py
============================
Problema 1: Verificação de expressões em sentenças.

Este módulo contém as funções para identificar a presença de expressões predefinidas
no início das sentenças de um texto.

Funções:
- encontra_expressoes: processa textos e identifica expressões no início de cada sentença
"""
from typing import List, Dict, Any

from analizador_de_texto.utils import ler_expressoes, separar_sentencas, verificar_expressao_inicio

def encontra_expressoes(
    informacoes_textos: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Analisa textos, identifica sentenças e verifica a presença de expressões em seus inícios.

    Args:
        informacoes_textos (List[Dict[str, Any]]): Lista de dicionários com 'id' e 'texto'.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários com 'id' e 'sentenças', onde 'sentenças'
        é uma lista de dicionários com 'sentença' e 'expressão'.
    """
    # Carrega as expressões
    expressoes = ler_expressoes()
    resultado = []

    for info_texto in informacoes_textos:
        id_texto = info_texto["id"]
        texto = info_texto["texto"]
        # Divide o texto em sentenças
        sentencas = separar_sentencas(texto)

        # Lista para armazenar as sentenças analisadas
        sentencas_analisadas = []

        # Analisa cada sentença
        for sentenca in sentencas:
            # Procura expressões no início da sentença
            expressao_encontrada = verificar_expressao_inicio(
                sentenca, expressoes
            )

            # Adiciona o resultado para esta sentença
            sentencas_analisadas.append({
                "sentenca": sentenca,
                "expressao": expressao_encontrada
            })

        # Adiciona o resultado para este texto
        resultado.append({
            "id": id_texto,
            "sentencas": sentencas_analisadas
        })

    return resultado

if __name__ == '__main__':
    from analizador_de_texto.utils import ler_entrada_json
    dados_entrada = ler_entrada_json("entrada.json")
    resultado = encontra_expressoes(dados_entrada)
    print(resultado)