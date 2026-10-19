"""Testes das validações e da limpeza do formulário de crédito."""

import pytest


@pytest.mark.parametrize(
    "idade,renda,valor,campos_invalidos",
    [
        pytest.param(
            "", "3000,00", "10000,00",
            ["idade"],
            id="idade-obrigatoria",
        ),
        pytest.param(
            "30", "", "10000,00",
            ["rendaMensal"],
            id="renda-obrigatoria",
        ),
        pytest.param(
            "30", "3000,00", "",
            ["valorSolicitado"],
            id="valor-obrigatorio",
        ),
        pytest.param(
            "", "", "",
            ["idade", "rendaMensal", "valorSolicitado"],
            id="todos-os-campos-obrigatorios",
        ),
    ],
)
def test_deve_exigir_campos_obrigatorios(
    credito_page,
    idade,
    renda,
    valor,
    campos_invalidos,
):
    """Confere mensagens, sinalização e foco dos campos obrigatórios."""
    credito_page.preencher_solicitacao(idade, renda, valor)
    credito_page.analisar()

    for campo in campos_invalidos:
        assert (
            credito_page.obter_erro_campo(campo)
            == "Este campo é obrigatório."
        )
        assert credito_page.campo_esta_invalido(campo)

    assert credito_page.obter_erros_visiveis() == {
        campo: "Este campo é obrigatório."
        for campo in campos_invalidos
    }
    assert (
        credito_page.obter_campo_em_foco()
        == campos_invalidos[0]
    )
    credito_page.aguardar_resultado_oculto()


@pytest.mark.parametrize(
    "idade,renda,valor,campo,mensagem",
    [
        pytest.param(
            "-1", "3000,00", "10000,00",
            "idade",
            "Informe uma idade inteira entre 0 e 120.",
            id="idade-negativa",
        ),
        pytest.param(
            "121", "3000,00", "10000,00",
            "idade",
            "Informe uma idade inteira entre 0 e 120.",
            id="idade-acima-do-maximo",
        ),
        pytest.param(
            "18.5", "3000,00", "10000,00",
            "idade",
            "Informe uma idade inteira entre 0 e 120.",
            id="idade-fracionaria",
        ),
        pytest.param(
            "abc", "3000,00", "10000,00",
            "idade",
            "Informe uma idade inteira entre 0 e 120.",
            id="idade-com-texto",
        ),
        pytest.param(
            "30", "0", "10000,00",
            "rendaMensal",
            "Informe um valor maior que zero e dentro do limite numérico.",
            id="renda-zero",
        ),
        pytest.param(
            "30", "3000,001", "10000,00",
            "rendaMensal",
            "Informe um valor numérico com no máximo duas casas decimais.",
            id="renda-com-tres-casas",
        ),
        pytest.param(
            "30", "abc", "10000,00",
            "rendaMensal",
            "Informe um valor numérico com no máximo duas casas decimais.",
            id="renda-com-texto",
        ),
        pytest.param(
            "30", "3000,00", "0",
            "valorSolicitado",
            "Informe um valor maior que zero e dentro do limite numérico.",
            id="valor-zero",
        ),
        pytest.param(
            "30", "3000,00", "10000,001",
            "valorSolicitado",
            "Informe um valor numérico com no máximo duas casas decimais.",
            id="valor-com-tres-casas",
        ),
        pytest.param(
            "30", "3000,00", "abc",
            "valorSolicitado",
            "Informe um valor numérico com no máximo duas casas decimais.",
            id="valor-com-texto",
        ),
    ],
)
def test_deve_rejeitar_dados_invalidos(
    credito_page,
    idade,
    renda,
    valor,
    campo,
    mensagem,
):
    """Confere a validação apresentada antes da análise de crédito."""
    credito_page.preencher_solicitacao(idade, renda, valor)
    credito_page.analisar()

    assert credito_page.obter_erro_campo(campo) == mensagem
    assert credito_page.campo_esta_invalido(campo)
    assert credito_page.obter_erros_visiveis() == {
        campo: mensagem,
    }
    assert credito_page.obter_campo_em_foco() == campo
    credito_page.aguardar_resultado_oculto()


@pytest.mark.parametrize(
    "renda,valor",
    [
        pytest.param(
            "3000,50", "10000,25",
            id="separador-virgula",
        ),
        pytest.param(
            "3000.50", "10000.25",
            id="separador-ponto",
        ),
    ],
)
def test_deve_aceitar_separadores_decimais(
    credito_page,
    renda,
    valor,
):
    """Permite valores monetários com vírgula ou ponto decimal."""
    credito_page.preencher_solicitacao("30", renda, valor)
    credito_page.analisar()
    credito_page.aguardar_resultado()

    assert credito_page.obter_status() == "APROVADO"
    assert credito_page.obter_motivos() == []
    assert credito_page.obter_erros_visiveis() == {}


def conferir_formulario_limpo(credito_page):
    """Confere campos vazios, ausência de erros e foco inicial."""
    for campo in ("idade", "rendaMensal", "valorSolicitado"):
        assert credito_page.obter_valor_campo(campo) == ""
        assert not credito_page.campo_esta_invalido(campo)

    assert credito_page.obter_erros_visiveis() == {}
    assert credito_page.obter_campo_em_foco() == "idade"
    credito_page.aguardar_resultado_oculto()


def test_deve_limpar_formulario_apos_resultado(credito_page):
    """Remove os dados e oculta uma análise já apresentada."""
    credito_page.preencher_solicitacao(
        "30",
        "3000,00",
        "10000,00",
    )
    credito_page.analisar()
    credito_page.aguardar_resultado()

    assert credito_page.obter_status() == "APROVADO"

    credito_page.limpar()

    conferir_formulario_limpo(credito_page)


def test_deve_limpar_mensagens_de_validacao(credito_page):
    """Remove as mensagens e a sinalização de campos inválidos."""
    credito_page.analisar()

    for campo in ("idade", "rendaMensal", "valorSolicitado"):
        assert (
            credito_page.obter_erro_campo(campo)
            == "Este campo é obrigatório."
        )
        assert credito_page.campo_esta_invalido(campo)

    credito_page.limpar()

    conferir_formulario_limpo(credito_page)
