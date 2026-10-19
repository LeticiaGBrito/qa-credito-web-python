"""Aplicação local, navegador, fixtures e evidências de falhas."""

import base64
import os
import socket
import threading
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
from uuid import uuid4

import pytest
import pytest_html
import uvicorn
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.credito_page import CreditoPage


@pytest.fixture(name="base_url", scope="session")
def fixture_base_url():
    """Inicia a aplicação local ou utiliza BASE_URL quando informada."""
    endereco_externo = os.getenv("BASE_URL", "").strip()

    if endereco_externo:
        yield endereco_externo.rstrip("/")
        return

    # Reserva uma porta disponível e mantém o socket aberto,
    # evitando que outro processo utilize a porta antes do servidor.
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.bind(("127.0.0.1", 0))
    porta = conexao.getsockname()[1]

    endereco = f"http://127.0.0.1:{porta}"
    raiz = Path(__file__).resolve().parents[1]
    pasta_relatorios = raiz / "reports"
    pasta_relatorios.mkdir(parents=True, exist_ok=True)

    configuracao = uvicorn.Config(
        app="app.credito_api:app",
        host="127.0.0.1",
        port=porta,
        log_level="info",
        access_log=False,
    )
    servidor = uvicorn.Server(configuracao)

    def executar_servidor():
        """Executa a aplicação utilizando o socket reservado."""
        servidor.run(sockets=[conexao])

    thread = threading.Thread(
        target=executar_servidor,
        name="aplicacao-demonstrativa",
        daemon=True,
    )

    try:
        thread.start()
        limite = time.monotonic() + 30
        disponivel = False

        while time.monotonic() < limite:
            if not thread.is_alive():
                pytest.fail(
                    "A aplicação encerrou durante a inicialização. "
                    "Confira os erros apresentados no terminal."
                )

            try:
                with urlopen(
                    f"{endereco}/health",
                    timeout=1,
                ) as resposta:
                    saude_ok = resposta.status == 200

                with urlopen(
                    f"{endereco}/simulador",
                    timeout=1,
                ) as resposta:
                    pagina_ok = resposta.status == 200

                if saude_ok and pagina_ok:
                    disponivel = True
                    break
            except (URLError, TimeoutError):
                pass

            time.sleep(0.1)

        if not disponivel:
            pytest.fail(
                "A aplicação demonstrativa não ficou disponível "
                "em 30 segundos."
            )

        yield endereco

    finally:
        servidor.should_exit = True

        if thread.is_alive():
            thread.join(timeout=10)

        if thread.is_alive():
            servidor.force_exit = True
            thread.join(timeout=5)

        conexao.close()

        if thread.is_alive():
            pytest.fail(
                "A aplicação não encerrou dentro do prazo esperado."
            )


@pytest.fixture(name="driver")
def fixture_driver(base_url):
    """Abre o Chrome após a aplicação estar disponível."""
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
