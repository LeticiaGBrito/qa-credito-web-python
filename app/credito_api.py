# Endpoints HTTP e disponibilização da interface
"""API HTTP educacional para análise fictícia de crédito."""

import json
from decimal import Decimal
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from app.analise_credito_service import AnaliseCreditoService


TAGS = [
    {
        "name": "Disponibilidade",
        "description": "Consulta de disponibilidade da aplicação.",
    },
    {
        "name": "Análise de crédito",
        "description": (
            "Análise de solicitações com critérios fictícios "
            "de idade, renda e valor solicitado."
        ),
    },
]

app = FastAPI(
    title="QA Crédito API — Python",
    description=(
        "API educacional de análise fictícia de crédito. "
        "As regras não representam políticas reais de concessão "
        "de crédito e não possuem vínculo com empresas. "
        "Utilize apenas dados fictícios."
    ),
    version="1.0.0",
    docs_url=None,
    openapi_tags=TAGS,
    servers=[
        {
            "url": "/",
            "description": "Servidor atual",
        }
    ],
)

service = AnaliseCreditoService()

# Caminho da interface demonstrativa utilizada pelos testes web.
PAGINA_WEB = Path(__file__).resolve().parent / "web" / "index.html"


@app.get(
    "/simulador",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def exibir_simulador() -> HTMLResponse:
    """Disponibiliza a interface educacional de análise de crédito."""
    return HTMLResponse(
        content=PAGINA_WEB.read_text(encoding="utf-8")
    )

# Mesma versão e configuração visual utilizadas no projeto Java.
SWAGGER_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>QA Crédito API — Python</title>

    <link
        rel="icon"
        type="image/svg+xml"
        href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23087f8c'/%3E%3Ctext x='32' y='33' dominant-baseline='middle' text-anchor='middle' font-family='Arial,sans-serif' font-size='30' font-weight='700' fill='white'%3ELG%3C/text%3E%3C/svg%3E"
    >

    <link
        rel="stylesheet"
        href="https://unpkg.com/swagger-ui-dist@5.32.0/swagger-ui.css"
    >

    <style>
        body {
            margin: 0;
            background: #fafafa;
        }

        .aviso {
            padding: 14px 20px;
            background: #e2f2ef;
            color: #123047;
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
        }

        .aviso a {
            color: #123047;
        }
    </style>
</head>

<body>
    <div class="aviso">
        <strong>Projeto educacional.</strong>
        Utilize apenas dados fictícios.
        As regras não representam políticas reais
        de concessão de crédito.
        <a href="/openapi.json">Consultar OpenAPI JSON</a>
    </div>

    <div id="swagger-ui"></div>

    <noscript>
        Ative o JavaScript para utilizar a documentação
        interativa da API.
    </noscript>

    <script
        src="https://unpkg.com/swagger-ui-dist@5.32.0/swagger-ui-bundle.js"
        crossorigin="anonymous"
    ></script>

    <script>
        window.onload = function () {
            if (typeof SwaggerUIBundle === "undefined") {
                document.getElementById("swagger-ui").textContent =
                    "Não foi possível carregar o Swagger UI. "
                    + "Verifique sua conexão com a internet.";
                return;
            }

            window.ui = SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui",
                deepLinking: true,
                displayRequestDuration: true,
                validatorUrl: null,
                persistAuthorization: false,
                presets: [
                    SwaggerUIBundle.presets.apis
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>
"""


def rejeitar_constante_invalida(valor: str) -> None:
    """Rejeita NaN e Infinity, que não são números válidos em JSON."""
    raise ValueError(f"Constante JSON inválida: {valor}.")


def ler_valor_monetario(dados: dict, campo: str) -> Decimal | None:
    """Obtém um número monetário sem aceitar textos ou booleanos."""
    valor = dados.get(campo)

    if valor is None:
        return None

    if isinstance(valor, bool) or not isinstance(valor, (int, Decimal)):
        raise ValueError(f"O campo {campo} deve ser numérico.")

    return Decimal(valor)


@app.get(
    "/docs",
    response_class=HTMLResponse,
    include_in_schema=False,
)
@app.get(
    "/docs/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def exibir_documentacao() -> HTMLResponse:
    """Disponibiliza a interface Swagger personalizada."""
    return HTMLResponse(content=SWAGGER_HTML)


@app.get(
    "/health",
    tags=["Disponibilidade"],
    summary="Consultar disponibilidade",
    description=(
        "Informa se a aplicação está respondendo. "
        "Não verifica banco de dados ou serviços externos."
    ),
    responses={
        200: {
            "description": "Aplicação disponível.",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Disponibilidade"
                    },
                    "example": {"status": "UP"},
                }
            },
        }
    },
)
def verificar_disponibilidade() -> dict[str, str]:
    """Informa que a aplicação está disponível."""
    return {"status": "UP"}


@app.post(
    "/analises-credito",
    tags=["Análise de crédito"],
    summary="Analisar solicitação de crédito",
    description=(
        "Uma solicitação válida é aprovada quando a idade é igual "
        "ou superior a 18 anos, a renda mensal é igual ou superior "
        "a R$ 2.000,00 e o valor solicitado não ultrapassa cinco "
        "vezes a renda. A reprovação por critérios de negócio "
        "também retorna HTTP 200, com os respectivos motivos."
    ),
    response_class=JSONResponse,
    responses={
        200: {
            "description": (
                "Análise realizada. Consulte o campo status "
                "para identificar aprovação ou reprovação."
            ),
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ResultadoAnalise"
                    },
                    "examples": {
                        "aprovado": {
                            "summary": "Crédito aprovado",
                            "value": {
                                "status": "APROVADO",
                                "motivos": [],
                            },
                        },
                        "reprovado": {
                            "summary": "Crédito reprovado por idade",
                            "value": {
                                "status": "REPROVADO",
                                "motivos": [
                                    "Solicitante deve ter pelo menos 18 anos."
                                ],
                            },
                        },
                    },
                }
            },
        },
        400: {
            "description": (
                "JSON malformado, campos obrigatórios ausentes "
                "ou dados inválidos."
            ),
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Erro"
                    },
                    "examples": {
                        "idadeInvalida": {
                            "summary": "Idade fora do intervalo permitido",
                            "value": {
                                "erro": (
                                    "Idade deve ser um número inteiro "
                                    "entre 0 e 120."
                                )
                            },
                        },
                        "jsonInvalido": {
                            "summary": "JSON malformado",
                            "value": {"erro": "JSON inválido."},
                        },
                    },
                }
            },
        },
        415: {
            "description": "Content-Type não aceito.",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Erro"
                    },
                    "example": {
                        "erro": "Utilize Content-Type application/json."
                    },
                }
            },
        },
    },
    openapi_extra={
        "requestBody": {
            "required": True,
            "description": (
                "Dados fictícios para análise. "
                "Todos os campos são obrigatórios."
            ),
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/SolicitacaoCredito"
                    },
                    "examples": {
                        "aprovacao": {
                            "summary": "Solicitação aprovada",
                            "value": {
                                "idade": 30,
                                "rendaMensal": 3000.00,
                                "valorSolicitado": 10000.00,
                            },
                        },
                        "limitesExatos": {
                            "summary": "Limites exatos de aprovação",
                            "value": {
                                "idade": 18,
                                "rendaMensal": 2000.00,
                                "valorSolicitado": 10000.00,
                            },
                        },
                        "reprovacaoPorIdade": {
                            "summary": "Reprovação por idade",
                            "value": {
                                "idade": 17,
                                "rendaMensal": 3000.00,
                                "valorSolicitado": 10000.00,
                            },
                        },
                        "multiplosMotivos": {
                            "summary": "Reprovação por múltiplos critérios",
                            "value": {
                                "idade": 17,
                                "rendaMensal": 1000.00,
                                "valorSolicitado": 6000.00,
                            },
                        },
                    },
                }
            },
        }
    },
)
async def analisar_credito(requisicao: Request) -> JSONResponse:
    """Valida a requisição e executa as regras de análise de crédito."""
    content_type = requisicao.headers.get("content-type", "")
    tipo_midia = content_type.split(";")[0].strip().lower()

    if tipo_midia != "application/json":
        return JSONResponse(
            status_code=415,
            content={"erro": "Utilize Content-Type application/json."},
        )

    corpo = await requisicao.body()

    try:
        dados = json.loads(
            corpo.decode("utf-8"),
            parse_float=Decimal,
            parse_constant=rejeitar_constante_invalida,
        )
    except (ValueError, UnicodeDecodeError):
        return JSONResponse(
            status_code=400,
            content={"erro": "JSON inválido."},
        )

    try:
        if not isinstance(dados, dict):
            raise ValueError(
                "O corpo da requisição deve ser um objeto JSON."
            )

        idade = dados.get("idade")
        renda = ler_valor_monetario(dados, "rendaMensal")
        valor = ler_valor_monetario(dados, "valorSolicitado")

        resultado = service.analisar(idade, renda, valor)

    except ValueError as erro:
        return JSONResponse(
            status_code=400,
            content={"erro": str(erro)},
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": resultado.status,
            "motivos": list(resultado.motivos),
        },
    )


def gerar_openapi_personalizado() -> dict:
    """Acrescenta modelos documentais à especificação do FastAPI."""
    if app.openapi_schema is not None:
        return app.openapi_schema

    especificacao = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        openapi_version=app.openapi_version,
        routes=app.routes,
        tags=TAGS,
        servers=app.servers,
    )

    modelos = especificacao.setdefault(
        "components", {}
    ).setdefault("schemas", {})

    modelos.update(
        {
            "Disponibilidade": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["UP"],
                        "description": (
                            "Estado de disponibilidade da aplicação."
                        ),
                    }
                },
            },
            "SolicitacaoCredito": {
                "type": "object",
                "required": [
                    "idade",
                    "rendaMensal",
                    "valorSolicitado",
                ],
                "properties": {
                    "idade": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 120,
                        "description": (
                            "Idade em anos. Envie um inteiro, como 30, "
                            "sem parte decimal. Para aprovação, "
                            "deve ser igual ou superior a 18."
                        ),
                        "example": 30,
                    },
                    "rendaMensal": {
                        "type": "number",
                        "exclusiveMinimum": 0,
                        "multipleOf": 0.01,
                        "description": (
                            "Renda mensal positiva, em reais, com "
                            "no máximo duas casas decimais na entrada. "
                            "Para aprovação, deve ser igual ou superior "
                            "a R$ 2.000,00."
                        ),
                        "example": 3000.00,
                    },
                    "valorSolicitado": {
                        "type": "number",
                        "exclusiveMinimum": 0,
                        "multipleOf": 0.01,
                        "description": (
                            "Valor solicitado positivo, em reais, com "
                            "no máximo duas casas decimais na entrada. "
                            "Para aprovação, não pode ultrapassar "
                            "cinco vezes a renda mensal."
                        ),
                        "example": 10000.00,
                    },
                },
            },
            "ResultadoAnalise": {
                "type": "object",
                "required": ["status", "motivos"],
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["APROVADO", "REPROVADO"],
                        "description": (
                            "Resultado da análise das regras de negócio."
                        ),
                    },
                    "motivos": {
                        "type": "array",
                        "description": (
                            "Motivos da reprovação. Lista vazia "
                            "quando a solicitação é aprovada."
                        ),
                        "items": {"type": "string"},
                    },
                },
            },
            "Erro": {
                "type": "object",
                "required": ["erro"],
                "properties": {
                    "erro": {
                        "type": "string",
                        "description": "Descrição do erro encontrado.",
                    }
                },
            },
        }
    )

    # Substitui o modelo inferido do retorno de /health
    # pela referência ao modelo documental nomeado.
    especificacao["paths"]["/health"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"] = {
        "$ref": "#/components/schemas/Disponibilidade"
    }

    app.openapi_schema = especificacao
    return especificacao


app.openapi = gerar_openapi_personalizado
