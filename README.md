## Descrição

Este projeto é uma solução para o desafio técnico da SOMOS Educação(https://gitlab.com/priscilla.lopes/desafio-dev-python-2025), implementando duas funcionalidades principais:

1. **Verificação de expressões em sentenças**: Identifica a presença de expressões predefinidas no início das sentenças de um texto.
2. **Categorização por base de regras**: Categoriza textos com base em regras predefinidas por especialistas.

## Instalação

### Via poetry

```bash
poetry add git+https://github.com/henriqueSpencer/desafio-somos-educacao.git
```

## Uso

### Verificação de expressões em sentenças

```python
from analizador_de_texto import encontra_expressoes

# Lista de textos para análise
textos = [
    {
        "id": 1,
        "texto": "Em primeiro lugar, a forma atual de ensino é importante. Logo, baseado no que foi dito, precisamos analisar melhor."
    }
]

# Analisar textos e encontrar expressões
resultados = encontra_expressoes(textos)
print(resultados)
```

Exemplo de saída:

```python
[
    {
        "id": 1,
        "sentencas": [
            {
                "sentenca": "Em primeiro lugar, a forma atual de ensino é importante.",
                "expressao": null
            },
            {
                "sentenca": "Logo, baseado no que foi dito, precisamos analisar melhor.",
                "expressao": "baseado no que foi dito"
            }
        ]
    }
]
```

### Categorização por base de regras

```python
from analizador_de_texto import aplica_regras

# Lista de textos para categorização
textos = [
    {
        "id": 1,
        "texto": "Em primeiro lugar, a forma atual de ensino é importante. Logo, baseado no que foi dito, precisamos analisar melhor. Pitágoras acreditava na importância da educação."
    }
]

# Categorizar textos
categorias = aplica_regras(textos)
print(categorias)
```

Exemplo de saída:

```python
[
    {
        "id": 1,
        "categorias": ["A"]
    }
]
```

## Estrutura de arquivos

Os arquivos de expressões e regras são esperados na pasta `analisador_de_texto/dados` com os seguintes nomes:

- `expressoes.txt`: Lista de expressões a serem verificadas (uma por linha)
- `regras_linguagem_natural.txt`: Regras para categorização em linguagem natural (uma por linha)


## Formato das regras

As regras de categorização devem seguir o formato:

```
Se [condição], então a categoria é [CATEGORIA].
```

Onde `[condição]` pode envolver:

- Número de sentenças: `número de sentenças é maior que 3`
- Número de tokens: `número de tokens é menor que 50`
- Presença de token: `"palavra" aparece no texto`
- Número de ocorrências: `número de "," é menor que 10`
- Presença de expressões: `não tem expressões`
- Número de sentenças com expressões: `número de sentenças com expressão é maior que 2`

Condições podem ser combinadas com o operador `E`:

```
Se número de tokens é maior que 90 E "Pitágoras" aparece no texto, então a categoria é A.
```

## Testes

Para executar os testes:

```bash
# Especificmaente os testes da utils:
poetry run pytest tests/test_utils.py
# Especificmaente os testes do problema 1:
poetry run pytest tests/test_problema1.py
# Especificmaente os testes do problema 2:
poetry run pytest tests/test_problema2.py

# Executando todos os testes:
poetry run pytest
```

## Autor

Henrique Spencer Albuquerque - [henriqueSpencer](https://github.com/henriqueSpencer)