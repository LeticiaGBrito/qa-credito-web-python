"""Page Object do simulador de análise de crédito."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CreditoPage(BasePage):
    """Representa os campos, ações e resultados do simulador."""

    IDADE = (By.ID, "idade")
    RENDA = (By.ID, "rendaMensal")
    VALOR = (By.ID, "valorSolicitado")

    ANALISAR = (By.ID, "analisar")
    LIMPAR = (By.ID, "limpar")

    RESULTADO = (By.ID, "resultado")
    TITULO_RESULTADO = (By.ID, "resultado-titulo")
    MOTIVOS = (By.CSS_SELECTOR, "#resultado-motivos li")

    CAMPOS = {
        "idade": IDADE,
        "rendaMensal": RENDA,
        "valorSolicitado": VALOR,
    }

    def abrir(self, base_url: str) -> None:
        """Abre o simulador e aguarda o formulário."""
        self.driver.get(f"{base_url.rstrip('/')}/simulador")
        self.aguardar_visivel(self.IDADE)

    def preencher_solicitacao(
        self,
        idade: str,
        renda: str,
        valor: str,
    ) -> None:
        """Preenche os dados de uma solicitação fictícia."""
        self.preencher(self.IDADE, idade)
        self.preencher(self.RENDA, renda)
        self.preencher(self.VALOR, valor)

    def analisar(self) -> None:
        """Envia o formulário pelo botão da interface."""
        self.clicar(self.ANALISAR)

    def limpar(self) -> None:
        """Aciona o botão que restaura o formulário."""
        self.clicar(self.LIMPAR)

    def aguardar_resultado(self) -> None:
        """Aguarda a apresentação do resultado da análise."""
        self.aguardar_visivel(self.RESULTADO)

    def aguardar_resultado_oculto(self) -> None:
        """Aguarda o painel de resultado ficar oculto."""
        self.wait.until(
            EC.invisibility_of_element_located(self.RESULTADO)
        )

    def obter_status(self) -> str | None:
        """Consulta o status apresentado no painel de resultado."""
        return self.aguardar_visivel(
            self.RESULTADO
        ).get_attribute("data-status")

    def obter_titulo_resultado(self) -> str:
        """Obtém o título visível do resultado."""
        return self.aguardar_visivel(
            self.TITULO_RESULTADO
        ).text

    def obter_motivos(self) -> list[str]:
        """Obtém os motivos apresentados na interface."""
        return [
            elemento.text
            for elemento in self.driver.find_elements(*self.MOTIVOS)
        ]

    def obter_erro_campo(self, campo: str) -> str:
        """Obtém a mensagem de validação de um campo."""
        localizador = (By.ID, f"{campo}-erro")

        return self.aguardar_visivel(localizador).text

    def obter_valor_campo(self, campo: str) -> str:
        """Consulta o valor atual de um campo do formulário."""
        elemento = self.aguardar_visivel(self.CAMPOS[campo])

        return elemento.get_property("value")

    def campo_esta_invalido(self, campo: str) -> bool:
        """Verifica a sinalização acessível de campo inválido."""
        elemento = self.aguardar_visivel(self.CAMPOS[campo])

        return elemento.get_attribute("aria-invalid") == "true"

    def obter_campo_em_foco(self) -> str | None:
        """Identifica o elemento que está com foco no navegador."""
        return self.driver.switch_to.active_element.get_attribute("id")

    def obter_erros_visiveis(self) -> dict[str, str]:
        """Retorna somente os campos com mensagens visíveis."""
        erros = {}

        for campo in self.CAMPOS:
            elemento = self.driver.find_element(
                By.ID,
                f"{campo}-erro",
            )

            if elemento.is_displayed() and elemento.text.strip():
                erros[campo] = elemento.text.strip()

        return erros
