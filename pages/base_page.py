"""Ações compartilhadas pelos Page Objects."""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Centraliza a interação com os elementos da página."""

    def __init__(self, driver: WebDriver, timeout: float = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def aguardar_visivel(self, localizador: tuple) -> WebElement:
        """Aguarda o elemento existir e estar visível."""
        return self.wait.until(
            EC.visibility_of_element_located(localizador)
        )

    def preencher(self, localizador: tuple, valor: str) -> None:
        """Limpa o campo antes de informar um novo valor."""
        elemento = self.aguardar_visivel(localizador)
        elemento.clear()
        elemento.send_keys(valor)

    def clicar(self, localizador: tuple) -> None:
        """Aguarda o elemento estar visível e habilitado."""
        elemento = self.wait.until(
            EC.element_to_be_clickable(localizador)
        )
        elemento.click()
