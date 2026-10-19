"""Configuração do navegador, fixtures e evidências de falhas."""

import base64
import os
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_html
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.credito_page import CreditoPage


@pytest.fixture(name="base_url")
def fixture_base_url() -> str:
    """Permite configurar o endereço sem alterar os testes."""
    return os.getenv(
        "BASE_URL",
        "http://127.0.0.1:8000",
    )


@pytest.fixture(name="driver")
def fixture_driver():
    """Configura o Chrome e encerra a sessão após cada teste."""
    opcoes = Options()
    headless = os.getenv("HEADLESS", "false").strip().lower() == "true"

    if headless:
        opcoes.add_argument("--headless=new")
        opcoes.add_argument("--window-size=1440,1000")
    else:
        opcoes.add_argument("--start-maximized")

    navegador = WebDriver(options=opcoes)

    try:
        if headless:
            navegador.set_window_size(1440, 1000)
        else:
            navegador.maximize_window()

        navegador.set_page_load_timeout(30)
        yield navegador
    finally:
        navegador.quit()


@pytest.fixture(name="credito_page")
def fixture_credito_page(driver, base_url):
    """Disponibiliza o simulador aberto para cada teste."""
    pagina = CreditoPage(driver, timeout=20)
    pagina.abrir(base_url)
    return pagina


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Anexa uma captura às falhas de preparação ou execução."""
    outcome = yield
    relatorio = outcome.get_result()

    if (
        not relatorio.failed
        or relatorio.when not in ("setup", "call")
    ):
        return

    navegador = item.funcargs.get("driver")

    if navegador is None:
        return

    extras = list(getattr(relatorio, "extras", []))

    try:
        imagem = navegador.get_screenshot_as_png()
    except WebDriverException as erro:
        extras.append(
            pytest_html.extras.text(
                str(erro),
                name="Não foi possível capturar a tela",
            )
        )
    else:
        imagem_base64 = base64.b64encode(imagem).decode("ascii")

        extras.append(
            pytest_html.extras.png(
                imagem_base64,
                name="Tela no momento da falha",
            )
        )

        pasta = Path(item.config.rootpath) / "reports" / "screenshots"
        arquivo = pasta / f"falha-{relatorio.when}-{uuid4().hex}.png"

        try:
            pasta.mkdir(parents=True, exist_ok=True)
            arquivo.write_bytes(imagem)
        except OSError as erro:
            extras.append(
                pytest_html.extras.text(
                    str(erro),
                    name="Não foi possível salvar o PNG separado",
                )
            )

    relatorio.extras = extras
