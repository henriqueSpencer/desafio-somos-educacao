"""utils.py
========================
Este módulo fornece funções auxiliares para processamento de texto e
manipulação de arquivos utilizadas.
"""
import json
from typing import List, Dict, Optional
import re
import os
import importlib.resources as pkg_resources

### PROBLEMA 1 ###
def caminho_amostras(nome_arquivo: str) -> str:
    """Retorna o caminho completo para um arquivo de amostras.

    Args:
        nome_arquivo (str): Nome do arquivo de amostras.

    Returns:
        str: Caminho completo para o arquivo de amostras.
    """
    try:
        # Tenta encontrar como recurso do pacote
        with pkg_resources.path('analizador_de_texto.dados', nome_arquivo) as p:
            return str(p)
    except (ImportError, ModuleNotFoundError):
        # Fallback para desenvolvimento local
        module_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(
            module_dir,
            'dados',
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

def ler_entrada_json(nome_arquivo: str = "entrada.json") -> Dict[str, str]:
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


### PROBLEMA 2 ###
def verificar_presenca_token(texto: str, token: str) -> bool:
    """Verifica se um token específico está presente no texto.

    Args:
        texto (str): Texto a ser analisado.
        token (str): Token a ser verificado.

    Returns:
        bool: True se o token estiver presente, False caso contrário.
    """
    return token.lower() in texto.lower()

def contar_tokens(texto: str) -> int:
    """Conta o número de tokens em um texto.

    Args:
        texto (str): Texto a ser analisado.

    Returns:
        int: Número de tokens no texto.
    """
    tokens = tokenize(texto)
    return len(tokens)

def contar_ocorrencias_token(texto: str, token: str) -> int:
    """Conta o número de ocorrências de um token específico no texto.

    Args:
        texto (str): Texto a ser analisado.
        token (str): Token a ser contado.

    Returns:
        int: Número de ocorrências do token no texto.
    """
    return texto.lower().count(token.lower())

def ler_regras(nome_arquivo: str = "regras_linguagem_natural.txt") -> List[str]:
    """Lê a lista de regras definida em um arquivo e retorna em formato de lista.

    Args:
        nome_arquivo (str): Nome do arquivo com regras.

    Returns:
        List[str]: Lista de regras em linguagem natural.
    """
    try:
        caminho_arquivo = caminho_amostras(nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            regras = [linha.strip() for linha in f if linha.strip()]
        return regras
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de regras não encontrado: {caminho_arquivo}")


















