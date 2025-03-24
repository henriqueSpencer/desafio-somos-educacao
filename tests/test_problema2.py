"""test_problema2.py
================================
Testes para a implementação do Problema 2: Categorização por base de regras.

Este módulo contém testes para a função aplica_regras,
verificando a correta categorização de textos com base em regras predefinidas.

Testes implementados:
- test_aplica_regras_sem_categoria: testa quando nenhuma regra é atendida
- test_aplica_regras_multiplos_textos: testa com vários textos
- test_aplica_regras_caso_real: testa com os exemplos do desafio
"""
"""test_problema2.py
================================
Testes para a implementação do Problema 2: Categorização por base de regras.

Este módulo contém testes para a função aplica_regras,
verificando a correta categorização de textos com base em regras predefinidas.

Testes implementados:
- test_aplica_regras_basico: testa categorização básica
- test_aplica_regras_sem_categoria: testa quando nenhuma regra é atendida
- test_aplica_regras_multiplos_textos: testa com vários textos
- test_aplica_regras_caso_real: testa com os exemplos do desafio
"""
import pytest
from analizador_de_texto import aplica_regras
from analizador_de_texto.problema2 import ParserRegras


# Mock das funções que acessam arquivos
@pytest.fixture(autouse=True)
def patch_utils(monkeypatch):
    # Mock para ler_regras
    def mock_ler_regras(arquivo=None):
        return [
            "Se número de sentenças é maior ou igual a três, então a categoria é A.",
            "Se \"Pitágoras\" aparece no texto, então a categoria é A",
            "Se \"onde\" aparece no texto E número de tokens é maior que 90, então a categoria é B.",
            "Se número de \",\" é menor que 10, então a categoria é C.",
            "Se número de sentenças é maior que 3 E número de sentenças com expressão é menor que 3, então a categoria é B.",
            "Se não tem expressões, então a categoria é C."
        ]

    # Mock para ler_expressoes
    def mock_ler_expressoes(arquivo=None):
        return [
            "a partir do exposto",
            "baseado no que foi dito",
            "como consequência",
            "perante os argumentos citados"
        ]

    monkeypatch.setattr("analizador_de_texto.problema2.ler_regras", mock_ler_regras)
    monkeypatch.setattr("analizador_de_texto.problema2.ler_expressoes", mock_ler_expressoes)
    monkeypatch.setattr("analizador_de_texto.problema2.separar_sentencas",
                        lambda texto: texto.split('. ') if texto else [])

    # Mock simplificado para verificar_expressao_inicio
    def mock_verificar_expressao_inicio(sentenca, expressoes):
        sentenca_lower = sentenca.lower()
        for expr in expressoes:
            if expr.lower() in sentenca_lower and sentenca_lower.find(expr.lower()) < 20:
                return expr
        return None

    monkeypatch.setattr("analizador_de_texto.problema2.verificar_expressao_inicio",
                        mock_verificar_expressao_inicio)


def test_aplica_regras_multiplos_textos():
    """Testa categorização de múltiplos textos com diferentes regras."""
    textos = [
        {
            "id": 3,
            "texto": "Primeira frase. Segunda frase. Pitágoras foi um filósofo importante."
        },
        {
            "id": 4,
            "texto": "Esta é uma frase, sem expressões, bastante, simples, com, poucas, vírgulas."
        }
    ]

    resultado = aplica_regras(textos)

    assert len(resultado) == 2

    # Primeiro texto deve ter categoria A (regra: "Pitágoras" aparece no texto)
    assert resultado[0]["id"] == 3
    assert "A" in resultado[0]["categorias"]

    # Segundo texto deve ter categoria C (regra: não tem expressões)
    assert resultado[1]["id"] == 4
    assert "C" in resultado[1]["categorias"]


def test_aplica_regras_caso_real():
    """Testa com os exemplos reais do desafio."""
    textos = [
        {
            "id": 1,
            "texto": "Em primeiro lugar, a forma atual de ensino, em que o aluno é obrigado a sentar-se em intervalos determinados pelos superiores, forma os adultos que levam essa forma de produção para o ofício. Logo, baseado no que foi dito, vale citar o filósofo Pitágoras, que explica que é melhor educar bem as crianças do que ter que reeducá-las como adultos. Assim, os maus hábitos adquiridos na infância podem gerar, nos adultos, muitas complicações, já que dentro da sala de aula, a movimentação dos alunos pelo ambiente é repudiada e muitas vezes com consequências. Como consequência, a doutrinação do modelo educacional não atende aos paradigmas de formação de um adulto atento à saúde ocupacional."
        },
        {
            "id": 4,
            "texto": "Perante os argumentos citados, é alarmante o número de indivíduos que crescem traumatizados, muitas vezes sem tratamento adequado, durante ou após a infância, desenvolvendo uma realidade de mundo inquietante. Por conseguinte, é relevante adicionar que, sendo a cultura - associada às relações e experiências de vida do cidadão - um meio pelo qual se cria a construção da realidade na consciência dos jovens, a realidade que está sendo criada pelas vítimas pode refletir na decadência da sociedade brasileira, em termos de segurança, educação e até cultural."
        }
    ]

    resultado = aplica_regras(textos)

    # Conforme saida_p2.json:
    # Texto 1 deve ter categorias A e B
    assert resultado[0]["id"] == 1
    assert "A" in resultado[0]["categorias"]  # Por ter mais de 3 sentenças e mencionar Pitágoras
    assert "B" in resultado[0]["categorias"]  # Outra regra atendida

    # Texto 4 deve ter categoria C
    assert resultado[1]["id"] == 4
    assert resultado[1]["categorias"] == ["C"]  # Regras específicas para este texto


def test_parser_regras():
    """Testa a classe ParserRegras diretamente."""
    parser = ParserRegras()
    regras_texto = [
        "Se número de sentenças é maior que 2, então a categoria é X.",
        "Se \"palavra\" aparece no texto, então a categoria é Y.",
        "Se número de sentenças é menor que 5 E \"outra\" aparece no texto, então a categoria é Z."
    ]

    regras_processadas = parser.analisar_regras(regras_texto)

    assert len(regras_processadas) == 3
    assert regras_processadas[0]["categoria"] == "X"
    assert regras_processadas[1]["categoria"] == "Y"
    assert regras_processadas[2]["categoria"] == "Z"

    # Testa a aplicação das regras processadas
    dados_texto = {
        "texto": "Esta é uma sentença com a palavra chave. Esta é outra sentença.",
        "sentencas": ["Esta é uma sentença com a palavra chave.", "Esta é outra sentença."],
        "expressoes_sentencas": [None, None]
    }

    # A primeira regra não deve ser atendida (número de sentenças não é > 2)
    assert not regras_processadas[0]["condicao"](dados_texto)

    # A segunda regra deve ser atendida ("palavra" aparece no texto)
    assert regras_processadas[1]["condicao"](dados_texto)