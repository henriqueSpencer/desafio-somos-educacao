# Utils é onde são colocadas as funções auxiliares

import json
from typing import List, Dict, Optional, Callable, Any, Union, Tuple
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

class ParserRegras:
    """Classe para analisar e processar regras em linguagem natural."""

    def __init__(self):
        """Inicializa o parser de regras."""
        # Padrões para identificar condições nas regras
        self.padroes_condicoes = {
            r'número de sentenças é (maior|menor|igual|maior ou igual|menor ou igual) (a|que) (\d+)': self._processar_qtd_sentencas,
            r'número de tokens é (maior|menor|igual|maior ou igual|menor ou igual) (a|que) (\d+)': self._processar_qtd_tokens,
            r'"([^"]+)" aparece no texto': self._processar_presenca_token,
            r'número de "([^"]+)" é (maior|menor|igual|maior ou igual|menor ou igual) (a|que) (\d+)': self._processar_qtd_token,
            r'número de sentenças com expressão é (maior|menor|igual|maior ou igual|menor ou igual) (a|que) (\d+)': self._processar_qtd_sentencas_expressao,
            r'não tem expressões': self._processar_sem_expressoes
        }

    def analisar_regras(self, regras_texto: List[str]) -> List[Dict[str, Any]]:
        """Analisa regras em texto e as converte em funções de condição.

        Args:
            regras_texto (List[str]): Lista de regras em linguagem natural.

        Returns:
            List[Dict[str, Any]]: Lista de dicionários com funções de condição e categorias.
        """
        regras_processadas = []

        for regra_texto in regras_texto:
            # Extrai a condição e a categoria da regra
            match = re.match(r'Se (.*), então a categoria é ([A-Za-z0-9]+)\.?', regra_texto)
            if match:
                condicao_texto = match.group(1)
                categoria = match.group(2)

                # Processa condições compostas (com E)
                if ' E ' in condicao_texto:
                    sub_condicoes = condicao_texto.split(' E ')
                    funcoes_condicao = [
                        self._analisar_condicao(cond.strip())
                        for cond in sub_condicoes
                    ]

                    # Cria uma função composta que verifica todas as sub-condições
                    def condicao_composta(dados_texto, funcs=funcoes_condicao):
                        return all(func(dados_texto) for func in funcs if func is not None)

                    funcao_condicao = condicao_composta
                else:
                    # Processa condição simples
                    funcao_condicao = self._analisar_condicao(condicao_texto)

                # Adiciona a regra processada à lista
                if funcao_condicao:
                    regras_processadas.append({
                        'condicao': funcao_condicao,
                        'categoria': categoria
                    })

        return regras_processadas

    def _analisar_condicao(self, condicao_texto: str) -> Optional[Callable]:
        """Analisa uma condição em texto e a converte em uma função.

        Args:
            condicao_texto (str): Condição em texto.

        Returns:
            Optional[Callable]: Função que implementa a condição ou None se a condição não for reconhecida.
        """
        # Tenta cada padrão de condição
        for padrao, processador in self.padroes_condicoes.items():
            match = re.match(padrao, condicao_texto)
            if match:
                return processador(*match.groups())

        # Se nenhum padrão corresponder
        print(f"AVISO: Condição não reconhecida: {condicao_texto}")
        return None

    def _processar_qtd_sentencas(self, operador: str, preposicao: str, valor: str) -> Callable:
        """Processa condição sobre quantidade de sentenças.

        Args:
            operador (str): Operador de comparação (maior, menor, igual, etc.).
            preposicao (str): Preposição ('a' ou 'que').
            valor (str): Valor numérico para comparação.

        Returns:
            Callable: Função que implementa a condição.
        """
        valor_int = int(valor)

        def verificar_qtd_sentencas(dados_texto):
            qtd_sentencas = len(dados_texto['sentencas'])
            return self._comparar(qtd_sentencas, operador, valor_int)

        return verificar_qtd_sentencas

    def _processar_qtd_tokens(self, operador: str, preposicao: str, valor: str) -> Callable:
        """Processa condição sobre quantidade de tokens.

        Args:
            operador (str): Operador de comparação (maior, menor, igual, etc.).
            preposicao (str): Preposição ('a' ou 'que').
            valor (str): Valor numérico para comparação.

        Returns:
            Callable: Função que implementa a condição.
        """
        valor_int = int(valor)

        def verificar_qtd_tokens(dados_texto):
            qtd_tokens = contar_tokens(dados_texto['texto'])
            return self._comparar(qtd_tokens, operador, valor_int)

        return verificar_qtd_tokens

    def _processar_presenca_token(self, token: str) -> Callable:
        """Processa condição sobre presença de token específico.

        Args:
            token (str): Token a ser verificado.

        Returns:
            Callable: Função que implementa a condição.
        """

        def verificar_presenca_token_a(dados_texto):
            return verificar_presenca_token(dados_texto['texto'], token)

        return verificar_presenca_token_a

    def _processar_qtd_token(self, token: str, operador: str, preposicao: str, valor: str) -> Callable:
        """Processa condição sobre quantidade de ocorrências de um token.

        Args:
            token (str): Token a ser contado.
            operador (str): Operador de comparação (maior, menor, igual, etc.).
            preposicao (str): Preposição ('a' ou 'que').
            valor (str): Valor numérico para comparação.

        Returns:
            Callable: Função que implementa a condição.
        """
        valor_int = int(valor)

        def verificar_qtd_token(dados_texto):
            qtd = contar_ocorrencias_token(dados_texto['texto'], token)
            return self._comparar(qtd, operador, valor_int)

        return verificar_qtd_token

    def _processar_qtd_sentencas_expressao(self, operador: str, preposicao: str, valor: str) -> Callable:
        """Processa condição sobre quantidade de sentenças com expressões.

        Args:
            operador (str): Operador de comparação (maior, menor, igual, etc.).
            preposicao (str): Preposição ('a' ou 'que').
            valor (str): Valor numérico para comparação.

        Returns:
            Callable: Função que implementa a condição.
        """
        valor_int = int(valor)

        def verificar_qtd_sentencas_expressao(dados_texto):
            qtd = sum(1 for expr in dados_texto['expressoes_sentencas'] if expr is not None)
            return self._comparar(qtd, operador, valor_int)

        return verificar_qtd_sentencas_expressao

    def _processar_sem_expressoes(self) -> Callable:
        """Processa condição sobre ausência de expressões.

        Returns:
            Callable: Função que implementa a condição.
        """

        def verificar_sem_expressoes(dados_texto):
            return all(expr is None for expr in dados_texto['expressoes_sentencas'])

        return verificar_sem_expressoes

    def _comparar(self, valor1: int, operador: str, valor2: int) -> bool:
        """Realiza comparação entre dois valores com base no operador.

        Args:
            valor1 (int): Primeiro valor.
            operador (str): Operador de comparação (maior, menor, igual, etc.).
            valor2 (int): Segundo valor.

        Returns:
            bool: Resultado da comparação.
        """
        if operador == 'maior':
            return valor1 > valor2
        elif operador == 'menor':
            return valor1 < valor2
        elif operador == 'igual':
            return valor1 == valor2
        elif operador == 'maior ou igual':
            return valor1 >= valor2
        elif operador == 'menor ou igual':
            return valor1 <= valor2
        else:
            return False

def aplica_regras(informacoes_textos: List[Dict[str, Any]],
                  arquivo_regras: str = "regras_linguagem_natural.txt",
                  arquivo_expressoes: str = "expressoes.txt") -> List[Dict[str, Any]]:
    """Categoriza textos com base em regras predefinidas.

    Args:
        informacoes_textos (List[Dict[str, Any]]): Lista de dicionários com 'id' e 'texto'.
        arquivo_regras (str, optional): Nome do arquivo com regras. Padrão: "regras_linguagem_natural.txt".
        arquivo_expressoes (str, optional): Nome do arquivo com expressões. Padrão: "expressoes.txt".

    Returns:
        List[Dict[str, Any]]: Lista de dicionários com 'id' e 'categorias'.
    """
    # Carrega as regras e expressões
    regras_texto = ler_regras(arquivo_regras)
    expressoes = ler_expressoes(arquivo_expressoes)

    # Analisa as regras
    parser = ParserRegras()
    regras = parser.analisar_regras(regras_texto)

    resultado = []
    # Processa cada texto
    for info_texto in informacoes_textos:
        id_texto = info_texto["id"]
        texto = info_texto["texto"]

        # Divide o texto em sentenças
        sentencas = separar_sentencas(texto)

        # Identifica expressões nas sentenças
        expressoes_encontradas = [
            verificar_expressao_inicio(sentenca, expressoes)
            for sentenca in sentencas
        ]

        # Prepara os dados para aplicação das regras verificar_presenca_token
        dados_texto = {
            'id': id_texto,
            'texto': texto,
            'sentencas': sentencas,
            'expressoes_sentencas': expressoes_encontradas
        }

        # Aplica as regras para determinar categorias
        categorias = set()
        for regra in regras:
            if regra['condicao'](dados_texto):
                categorias.add(regra['categoria'])

        # Adiciona o resultado para este texto
        resultado.append({
            'id': id_texto,
            'categorias': sorted(list(categorias))
        })

    return resultado

if __name__ == '__main__':
    # Resolucao Problema 1
    dados_entrada = ler_entrada_json("entrada.json")
    resultado = encontra_expressoes(dados_entrada)
    print(resultado)

    # Resolucao Problema 2
    dados_entrada = ler_entrada_json()
    resultado = aplica_regras(dados_entrada)
    print(resultado)


















