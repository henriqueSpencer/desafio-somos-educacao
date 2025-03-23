# Utils é onde são colocadas as funções auxiliares

import json
from typing import List, Dict, Optional, Callable
from typing import List, Dict, Any, Optional, Union, Tuple
import re
import os

### PROBLEMA 1 ###
def caminho_amostras(nome_arquivo: str) -> str:
    """Retorna o caminho completo para um arquivo de amostras.

    Args:
        nome_arquivo (str): Nome do arquivo de amostras.

    Returns:
        str: Caminho completo para o arquivo de amostras.
    """
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        os.path.dirname(module_dir),
        'amostras',
        nome_arquivo
    )

def ler_expressoes(nome_arquivo: str = "expressoes.txt") -> List[List[str]]:
    """Lê a lista de expressões definida em um arquivo e retorna em formato de lista.

    Args:
        nome_arquivo (str): Nome do arquivo com expressões.

    Returns:
        str: Lista de expressões.
    """
    try:
        caminho_arquivo = caminho_amostras(nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            expressoes = [linha.strip() for linha in f if linha.strip()]
        return expressoes
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de expressões não encontrado: {caminho_arquivo}")

def ler_entrada_json(nome_arquivo: str) -> Dict[str, str]:
    """Lê o arquivo de entrada JSON com textos para análise.

    Args:
        nome_arquivo (str): Nome do arquivo de entrada.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários com textos e seus identificadores.
    """
    try:
        caminho_arquivo = caminho_amostras(nome_arquivo)
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho_arquivo}")
    except json.JSONDecodeError:
        raise ValueError(f"Formato JSON inválido no arquivo: {caminho_arquivo}")

def separar_sentencas(texto: str) -> List[str]:
    """Separa um texto em sentenças (frases delimitadas por .?!).

    Args:
        texto (str): Texto a ser separado em sentenças.

    Returns:
        List[str]: Lista de sentenças.
    """
    sentencas = re.findall(r'[^.?!]+[.?!]', texto)
    return [s.strip() for s in sentencas]

def tokenize(sentence: str) -> List[str]:
    """Divide uma sentença em tokens.

    Args:
        sentence: Sentença a ser tokenizada.

    Returns:
        List[str]: Lista de tokens.
    """
    # Preserva a pontuação como tokens separados
    pattern = r'(\w+|\S)'
    tokens = re.findall(pattern, sentence)

    # Remove tokens vazios
    return [token for token in tokens if token.strip()]


def verificar_expressao_inicio(sentenca: str, expressoes: List[str], max_tokens_inicio: int = 3) -> Optional[str]:
    """Verifica se uma expressão está presente no início da sentença.

    Args:
        sentenca (str): Sentença a ser verificada.
        expressoes (List[str]): Lista de expressões a serem procuradas.
        max_tokens_inicio (int): Número máximo de tokens considerados como início.

    Returns:
        Optional[str]: A expressão encontrada ou None se nenhuma for encontrada.
    """
    # Limita a verificação aos primeiros max_tokens_inicio tokens
    tokens_sentenca = tokenize(sentenca)

    # Texto completo em lowercase para verificação
    texto_lower = sentenca.lower()

    # Verifica cada expressão
    for expressao in expressoes:
        expressao_lower = expressao.lower()

        # Primeiro verificamos se a expressão aparece no texto em geral
        if expressao_lower in texto_lower:
            # Tokeniza a expressão
            tokens_expressao = tokenize(expressao_lower)

            # Verifica se a expressão começa em algum dos tokens iniciais
            for i in range(min(max_tokens_inicio, len(tokens_sentenca) - len(tokens_expressao) + 1)):
                # Compara os tokens da expressão com os tokens da sentença
                matched = True
                for j in range(len(tokens_expressao)):
                    if i + j >= len(tokens_sentenca) or tokens_sentenca[i + j].lower() != tokens_expressao[j]:
                        matched = False
                        break
                # Se encontrou uma correspondência, retorna a expressão original (mantendo capitalização)
                if matched:
                    return expressao

    return None

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
    dados_entrada = ler_entrada_json("entrada.json")
    resultado = encontra_expressoes(dados_entrada)
    print(resultado)



















