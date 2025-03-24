"""test_problema1.py
================================
Testes para a implementação do Problema 1: Verificação de expressões em sentenças.

Este módulo contém testes para a função encontra_expressoes, verificando
a correta identificação de expressões predefinidas no início das sentenças.

Testes implementados:
- test_encontra_expressoes_basico: verifica identificação básica de expressões
- test_encontra_expressoes_sem_expressoes: verifica quando não há expressões
- test_encontra_expressoes_multiplos_textos: testa com vários textos
- test_encontra_expressoes_caso_real: testa com os exemplos do desafio
- test_encontra_expressoes_vazio: testa com texto vazio
"""
import pytest
from analizador_de_texto import encontra_expressoes


# Mock da função ler_expressoes para usar expressões de teste
def mock_ler_expressoes():
    return [
        "a partir do exposto",
        "baseado no que foi dito",
        "como consequência",
        "perante os argumentos citados",
        "por fim"
    ]


# Patch das funções que acessam arquivos
@pytest.fixture(autouse=True)
def patch_utils(monkeypatch):
    monkeypatch.setattr("analizador_de_texto.problema1.ler_expressoes", mock_ler_expressoes)


def test_encontra_expressoes_basico():
    """Testa identificação de expressões básicas no início de sentenças."""
    textos = [
        {
            "id": 1,
            "texto": "Primeiro parágrafo. A partir do exposto, podemos concluir. Outra frase normal."
        }
    ]

    resultado = encontra_expressoes(textos)

    assert len(resultado) == 1
    assert resultado[0]["id"] == 1
    assert len(resultado[0]["sentencas"]) == 3

    # Verifica expressões
    assert resultado[0]["sentencas"][0]["expressao"] is None
    assert resultado[0]["sentencas"][1]["expressao"] == "a partir do exposto"
    assert resultado[0]["sentencas"][2]["expressao"] is None


def test_encontra_expressoes_sem_expressoes():
    """Testa texto sem nenhuma expressão predefinida."""
    textos = [
        {
            "id": 2,
            "texto": "Este texto não contém nenhuma das expressões listadas. Somente frases comuns."
        }
    ]

    resultado = encontra_expressoes(textos)

    assert len(resultado) == 1
    assert len(resultado[0]["sentencas"]) == 2

    # Todas as sentenças devem ter expressão None
    for sentenca in resultado[0]["sentencas"]:
        assert sentenca["expressao"] is None


def test_encontra_expressoes_multiplos_textos():
    """Testa processamento de múltiplos textos com diferentes expressões."""
    textos = [
        {
            "id": 3,
            "texto": "Texto simples. Por fim, uma conclusão."
        },
        {
            "id": 4,
            "texto": "Como consequência, o resultado é positivo. Baseado no que foi dito, podemos avançar."
        }
    ]

    resultado = encontra_expressoes(textos)

    assert len(resultado) == 2

    # Verifica primeiro texto
    assert resultado[0]["id"] == 3
    assert len(resultado[0]["sentencas"]) == 2
    assert resultado[0]["sentencas"][0]["expressao"] is None
    assert resultado[0]["sentencas"][1]["expressao"] == "por fim"

    # Verifica segundo texto
    assert resultado[1]["id"] == 4
    assert len(resultado[1]["sentencas"]) == 2
    assert resultado[1]["sentencas"][0]["expressao"] == "como consequência"
    assert resultado[1]["sentencas"][1]["expressao"] == "baseado no que foi dito"


def test_encontra_expressoes_caso_real():
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

    resultado = encontra_expressoes(textos)

    # Verificações do texto 1
    assert resultado[0]["id"] == 1
    assert len(resultado[0]["sentencas"]) == 4

    assert resultado[0]["sentencas"][0]["expressao"] is None
    assert resultado[0]["sentencas"][1]["expressao"] == "baseado no que foi dito"
    assert resultado[0]["sentencas"][2]["expressao"] is None
    assert resultado[0]["sentencas"][3]["expressao"] == "como consequência"

    # Verificações do texto 4
    assert resultado[1]["id"] == 4
    assert len(resultado[1]["sentencas"]) == 2

    assert resultado[1]["sentencas"][0]["expressao"] == "perante os argumentos citados"
    assert resultado[1]["sentencas"][1]["expressao"] is None


def test_encontra_expressoes_vazio():
    """Testa comportamento com texto vazio."""
    textos = [
        {
            "id": 5,
            "texto": ""
        }
    ]

    resultado = encontra_expressoes(textos)

    assert len(resultado) == 1
    assert resultado[0]["id"] == 5
    assert len(resultado[0]["sentencas"]) == 0
    assert resultado[0]["sentencas"] == []
