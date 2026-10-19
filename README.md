# QA Crédito Web — Python

[![Testes Web Python](https://github.com/LeticiaGBrito/qa-credito-web-python/actions/workflows/testes-web.yml/badge.svg?branch=main)](https://github.com/LeticiaGBrito/qa-credito-web-python/actions/workflows/testes-web.yml)

Projeto educacional de automação de testes web de um simulador
fictício de análise de crédito, utilizando Python, Selenium e pytest.

A suíte verifica a jornada pelo navegador, desde o preenchimento
do formulário até a apresentação do resultado, incluindo validações
de campos e limpeza da interface.

A aplicação e suas regras são fictícias, sem vínculo com empresas
ou políticas reais de concessão de crédito.

## Objetivo

Demonstrar a construção de uma automação web com:

- Page Objects e reutilização de ações.
- Esperas explícitas para sincronização com a interface.
- Cenários parametrizados e independentes.
- Validação de regras de negócio e valores de fronteira.
- Verificação de mensagens, foco e sinalização dos campos.
- Relatórios HTML e JUnit XML.
- Captura automática de tela em caso de falha.
- Execução em integração contínua com GitHub Actions.

## Aplicação testada

O simulador pertence a um projeto separado, desenvolvido com
Python e FastAPI.

- [Código da aplicação](https://github.com/LeticiaGBrito/qa-credito-api-python)
- [Simulador publicado](https://qa-credito-api-python.onrender.com/simulador)
- [Documentação da API](https://qa-credito-api-python.onrender.com/docs)

Na execução local padrão, a aplicação deve estar disponível em:

```text
http://127.0.0.1:8000/simulador
```

Na CI, o workflow baixa o repositório da aplicação e inicia uma
instância dentro do ambiente do GitHub Actions.

## Tecnologias e finalidade

| Tecnologia ou prática | Finalidade |
| --- | --- |
| Python | Implementação dos Page Objects, fixtures e testes |
| Selenium WebDriver | Controle do Chrome e interação com a interface |
| Selenium Manager | Gerenciamento do driver quando necessário |
| pytest | Descoberta, organização e execução dos testes |
| Parametrização | Execução do mesmo comportamento com diferentes dados |
| Fixtures | Preparação e encerramento do navegador |
| Page Object Model | Separação entre interação com a página e verificações dos testes |
| WebDriverWait | Espera por condições específicas da interface |
| pytest-html | Geração do relatório HTML com evidências |
| JUnit XML | Exportação dos resultados em formato compatível com ferramentas de CI |
| GitHub Actions | Execução automática dos testes |
| Git | Versionamento do código |

As dependências diretas estão registradas em
`requirements-dev.txt`.

## Organização dos arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `pages/__init__.py` | Identifica o pacote dos Page Objects |
| `pages/base_page.py` | Centraliza esperas explícitas e ações compartilhadas |
| `pages/credito_page.py` | Representa os campos, botões, mensagens e resultados do simulador |
| `tests/conftest.py` | Configura endereço, navegador, fixtures e capturas de falhas |
| `tests/test_solicitacao_credito.py` | Verifica aprovação e reprovação pela interface |
| `tests/test_validacao_formulario.py` | Verifica campos obrigatórios, entradas inválidas, separadores decimais e limpeza |
| `pytest.ini` | Configura descoberta dos testes e geração de relatórios |
| `requirements-dev.txt` | Registra as dependências da automação |
| `.github/workflows/testes-web.yml` | Define o fluxo de integração contínua |
| `.gitignore` | Exclui ambientes locais, caches e relatórios do versionamento |

### Classes principais

| Classe | Finalidade |
| --- | --- |
| `BasePage` | Disponibiliza ações reutilizáveis para aguardar, preencher e clicar |
| `CreditoPage` | Concentra os localizadores e as interações específicas do simulador |

As verificações dos resultados ficam nos testes, enquanto os
Page Objects concentram as interações e a leitura da interface.

## Regras fictícias de aprovação

A solicitação deve atender a todos os critérios:

- Idade igual ou superior a 18 anos.
- Renda mensal igual ou superior a R$ 2.000,00.
- Valor solicitado menor ou igual a cinco vezes a renda mensal.

Dados válidos que não atendem aos critérios geram uma análise
reprovada, com os respectivos motivos.

A interface também verifica campos obrigatórios, idade entre
0 e 120, valores monetários positivos e precisão de até duas
casas decimais.

## Estratégia de testes

A suíte atual possui **24 cenários automatizados**.

| Grupo | Quantidade |
| --- | ---: |
| Aprovação e limites exatos | 2 |
| Reprovação e múltiplos motivos | 4 |
| Campos obrigatórios | 4 |
| Entradas inválidas | 10 |
| Separadores decimais | 2 |
| Limpeza do formulário | 2 |
| **Total** | **24** |

### Solicitação de crédito

- Aprovação com dados válidos.
- Aprovação com idade, renda e valor nos limites exatos.
- Reprovação por idade inferior ao mínimo.
- Reprovação por renda inferior ao mínimo.
- Reprovação por valor acima do limite.
- Exibição de todos os motivos quando vários critérios falham.

### Campos obrigatórios

- Idade não preenchida.
- Renda mensal não preenchida.
- Valor solicitado não preenchido.
- Todos os campos não preenchidos.

Os testes conferem as mensagens, o atributo `aria-invalid`,
o foco no primeiro campo inválido e a ausência do painel
de resultado.

### Entradas inválidas

- Idade negativa.
- Idade superior a 120.
- Idade fracionária.
- Idade preenchida com texto.
- Renda igual a zero.
- Renda com três casas decimais.
- Renda preenchida com texto.
- Valor solicitado igual a zero.
- Valor solicitado com três casas decimais.
- Valor solicitado preenchido com texto.

### Formatos monetários

- Aceitação de vírgula como separador decimal.
- Aceitação de ponto como separador decimal.

### Botão Limpar

- Limpeza dos campos e ocultação do resultado após uma análise.
- Remoção das mensagens e da sinalização dos campos inválidos.
- Retorno do foco ao campo de idade.

## Isolamento e sincronização

Cada cenário utiliza uma nova sessão do Chrome, encerrada
ao final do teste.

A automação utiliza esperas explícitas para aguardar elementos
visíveis, botões habilitados e a apresentação ou ocultação
do resultado.

Não utiliza pausas fixas com `time.sleep` nos Page Objects
ou nos testes.

O workflow utiliza uma espera com tentativas limitadas para
verificar a disponibilidade da aplicação antes de iniciar a suíte.

## Pré-requisitos para execução local

- Python 3.13.
- Google Chrome instalado.
- Git, para clonar os repositórios.
- Acesso à internet para instalar dependências e, quando necessário,
  obter o driver.
- Aplicação de crédito em execução.

Não é necessário instalar o ChromeDriver manualmente na
configuração padrão.

## Preparar o projeto de automação

Execute os comandos em uma pasta de sua preferência:

```powershell
git clone https://github.com/LeticiaGBrito/qa-credito-web-python.git
Set-Location .\qa-credito-web-python
```

Crie o ambiente virtual:

```powershell
py -3.13 -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Não é necessário ativar o ambiente virtual quando seu executável
é utilizado explicitamente nos comandos.

## Iniciar a aplicação local

Em outro terminal, clone o projeto da aplicação em uma pasta
separada da automação:

```powershell
git clone https://github.com/LeticiaGBrito/qa-credito-api-python.git
Set-Location .\qa-credito-api-python
```

Se o repositório já estiver disponível, entre na pasta existente
em vez de cloná-lo novamente.

Prepare o ambiente da aplicação:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe -m uvicorn credito.credito_api:app --host 127.0.0.1 --port 8000
```

Mantenha esse terminal aberto durante os testes.

Para encerrar a aplicação, pressione `Ctrl + C`.

## Executar os testes

No terminal do projeto de automação:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Por padrão, o Chrome abre com interface visível e janela maximizada.

### Executar somente os cenários de aprovação

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_solicitacao_credito.py -k deve_aprovar
```

### Executar somente as validações do formulário

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validacao_formulario.py
```

## Configurações por variáveis de ambiente

| Variável | Padrão | Finalidade |
| --- | --- | --- |
| `BASE_URL` | `http://127.0.0.1:8000` | Define o endereço base da aplicação, sem `/simulador` |
| `HEADLESS` | `false` | Define se o Chrome será executado sem interface visível |

### Executar sem abrir a janela do navegador

```powershell
$env:HEADLESS = "true"
.\.venv\Scripts\python.exe -m pytest
```

No modo headless, a janela é configurada com dimensões de
1440 × 1000.

### Voltar à execução visível

```powershell
$env:HEADLESS = "false"
```

### Alterar o endereço da aplicação

```powershell
$env:BASE_URL = "http://127.0.0.1:8000"
```

As variáveis definidas dessa forma permanecem na sessão
atual do terminal.

## Execução em Linux ou macOS

Prepare o ambiente da automação:

```bash
python3.13 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
```

Com a aplicação disponível, execute:

```bash
HEADLESS=true BASE_URL=http://127.0.0.1:8000 \
./.venv/bin/python -m pytest
```

A aplicação também precisa ter seu próprio ambiente preparado
e estar em execução, conforme o README do repositório da API.

## Relatórios e evidências

| Caminho | Conteúdo |
| --- | --- |
| `reports/relatorio-testes.html` | Resultados para visualização no navegador |
| `reports/resultados.xml` | Resultados em formato JUnit XML |
| `reports/screenshots/` | Capturas PNG geradas em caso de falha |

Para abrir o relatório no Windows:

```powershell
Start-Process .\reports\relatorio-testes.html
```

O HTML e o XML são sobrescritos a cada execução.
As capturas PNG anteriores permanecem na pasta até serem removidas.

Os relatórios, as capturas e o ambiente virtual não são versionados.

### Captura automática de falhas

Quando um cenário falha na preparação ou na execução e existe
uma sessão de navegador disponível, a configuração tenta:

1. Capturar a tela atual do navegador.
2. Incorporar a imagem ao relatório HTML.
3. Salvar uma cópia PNG em `reports/screenshots`.

No relatório, a evidência aparece como
**Tela no momento da falha**.

Se a falha ocorrer antes da criação do navegador, não haverá
uma sessão disponível para capturar a tela.

A configuração atual não captura falhas da etapa de encerramento
das fixtures.

A captura mostra a área visível da página, não necessariamente
todo o seu conteúdo.

## Integração contínua

O workflow `testes-web.yml` está configurado para executar em:

- Push para `main`.
- Pull request direcionado a `main`.
- Acionamento manual por `workflow_dispatch`.

O fluxo realiza as seguintes etapas:

1. Baixa o repositório da automação.
2. Baixa a branch `main` do repositório da aplicação.
3. Configura o Python 3.13.
4. Registra o commit da aplicação que será testada.
5. Instala e verifica as dependências.
6. Confere a disponibilidade do Chrome.
7. Inicia a aplicação localmente no runner.
8. Aguarda os endpoints `/health` e `/simulador`.
9. Executa os testes com Chrome headless.
10. Encerra o processo da aplicação.
11. Publica os relatórios e evidências disponíveis como artefato.

O ambiente configurado é `ubuntu-24.04`, com limite de
15 minutos para o job.

A execução dos testes na CI não depende do Render nem
da máquina da autora ligada.

O workflow deste repositório implementa **integração contínua (CI)**.
Ele não realiza deploy da aplicação.

Alterações feitas somente no repositório da API não disparam
automaticamente este workflow web.

### Rastreabilidade da aplicação

A aplicação é obtida da branch `main`, que pode mudar entre
as execuções.

O commit efetivamente testado fica registrado no artefato:

```text
versao-aplicacao.txt
```

### Consultar os resultados no GitHub

1. Abra a aba **Actions**.
2. Selecione uma execução de **Testes Web Python**.
3. Abra o job **Selenium com Chrome** para consultar as etapas.
4. Em **Summary → Artifacts**, baixe
   `relatorios-testes-web-python`.
5. Extraia o ZIP antes de abrir o relatório HTML.

Os artefatos estão configurados para retenção de **14 dias**.

Além dos relatórios e das eventuais capturas, o workflow pode
disponibilizar:

- `servidor.log`: saída do servidor.
- `versao-aplicacao.txt`: commit da aplicação testada.
- `servidor.pid`: identificador do processo iniciado na execução.

A publicação dos arquivos disponíveis é tentada mesmo quando
uma etapa anterior falha.

## Limites do projeto

- Projeto educacional com dados e regras fictícias.
- Automação atualmente direcionada ao Chrome.
- Não utiliza dados reais de clientes.
- Não implementa uma política real de concessão de crédito.
- Não realiza testes de carga, segurança ou acessibilidade completos.
- A verificação de foco e `aria-invalid` cobre comportamentos
  específicos da interface, não uma auditoria de acessibilidade.
- Testes aprovados não significam ausência de defeitos
  ou cobertura total.
- Os tempos registrados representam a execução dos testes,
  não um benchmark de desempenho da aplicação.

## Autora

Letícia Gonçalves Garcia — QA Sênior

[Portfólio](https://leticiagbrito.github.io/)
