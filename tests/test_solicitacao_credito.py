"""Testes da jornada de solicitação de crédito pelo navegador."""

import pytest


@pytest.mark.parametrize(
    "idade,renda,valor",
    [
        pytest.param(
            "30",
            "3000,00",
            "10000,00",
            id="solicitacao-valida",
        ),
        pytest.param(
            "18",
            "2000,00",
            "10000,00",
            id="limites-exatos",
        ),
    ],
)
def test_deve_aprovar_solicitacao(
    credito_page,
    idade,
    renda,
    valor,
):
    """Verifica aprovação e ausência de motivos de reprovação."""
    credito_page.preencher_solicitacao(
        idade=idade,
        renda=renda,
        valor=valor,
    )

    credito_page.analisar()
    credito_page.aguardar_resultado()

    assert credito_page.obter_status() == "APROVADO"
    assert (
        credito_page.obter_titulo_resultado()
        == "Solicitação aprovada"
    )
    assert credito_page.obter_motivos() == []


@pytest.mark.parametrize(
    "idade,renda,valor,motivos",
    [
        pytest.param(
            "17",
            "3000,00",
            "10000,00",
            [
                "Solicitante deve ter pelo menos 18 anos.",
            ],
            id="menor-de-idade",
        ),
        pytest.param(
            "30",
            "1999,99",
            "5000,00",
            [
                "Renda mensal inferior a R$ 2.000,00.",
            ],
            id="renda-abaixo-do-minimo",
        ),
        pytest.param(
            "30",
            "3000,00",
            "15000,01",
            [
                "Valor solicitado superior a cinco vezes a renda mensal.",
            ],
            id="valor-acima-do-limite",
        ),
        pytest.param(
            "17",
            "1000,00",
            "6000,00",
            [
                "Solicitante deve ter pelo menos 18 anos.",
                "Renda mensal inferior a R$ 2.000,00.",
                "Valor solicitado superior a cinco vezes a renda mensal.",
            ],
            id="multiplos-motivos",
        ),
    ],
)
def test_deve_reprovar_solicitacao(
    credito_page,
    idade,
    renda,
    valor,
    motivos,
):
    """Verifica reprovação e os motivos exibidos ao usuário."""
    credito_page.preencher_solicitacao(
        idade=idade,
        renda=renda,
        valor=valor,
    )

    credito_page.analisar()
    credito_page.aguardar_resultado()

    assert credito_page.obter_status() == "REPROVADO"
    assert (
        credito_page.obter_titulo_resultado()
        == "Solicitação reprovada"
    )
    assert credito_page.obter_motivos() == motivos
