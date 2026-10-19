# QA Crédito Web — Python

[![Testes Web Python](https://github.com/LeticiaGBrito/qa-credito-web-python/actions/workflows/testes-web.yml/badge.svg?branch=main)](https://github.com/LeticiaGBrito/qa-credito-web-python/actions/workflows/testes-web.yml)

Projeto educacional de automação de testes web com Python,
Selenium e pytest, utilizando um simulador fictício de análise
de crédito.

O repositório inclui a aplicação demonstrativa e os testes.
Após instalar as dependências, um único comando inicia a aplicação,
executa os testes e encerra o servidor automaticamente.

As regras são fictícias e não representam políticas reais
de concessão de crédito. O projeto não possui vínculo com empresas.

## Objetivo

Demonstrar a transformação de requisitos e regras de negócio
em testes automatizados pela interface, contemplando:

- Aprovação e reprovação de solicitações.
- Valores de fronteira.
- Campos obrigatórios.
- Entradas inválidas.
- Mensagens de validação.
- Limpeza do formulário.
- Relatórios de execução e capturas de tela em caso de falha.
- Execução automatizada em integração contínua.

## Tecnologias e finalidade

| Tecnologia | Finalidade |
| --- | --- |
| Python | Implementação da aplicação demonstrativa e dos testes |
| Selenium WebDriver | Interação automatizada com o navegador |
| Selenium Manager | Gerenciamento do driver do navegador, quando necessário |
| pytest | Organização e execução dos testes |
| pytest-html | Geração do relatório HTML |
| JUnit XML | Formato de relatório para integração com ferramentas de CI |
| FastAPI | Disponibilização da aplicação e dos endpoints HTTP |
| Uvicorn | Execução do servidor local |
| Decimal | Representação dos valores monetários nas regras de negócio |
| HTML, CSS e JavaScript | Interface e comportamento do simulador |
| GitHub Actions | Execução dos testes em integração contínua |

As dependências estão registradas em:

- `requirements-app.txt`: dependências da aplicação demonstrativa.
- `requirements-dev.txt`: dependências da aplicação e dos testes.

## Organização dos arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `app/__init__.py` | Identifica o pacote da aplicação demonstrativa |
| `app/analise_credito_service.py` | Valida os dados e aplica as regras fictícias de crédito |
| `app/credito_api.py` | Disponibiliza a interface e os endpoints HTTP |
| `app/web/index.html` | Implementa o formulário do simulador |
| `pages/__init__.py` | Identifica o pacote dos Page Objects |
| `pages/base_page.py` | Centraliza ações reutilizáveis e esperas explícitas |
| `pages/credito_page.py` | Define os localizadores e as ações do simulador |
| `tests/conftest.py` | Configura a aplicação local, o navegador, as fixtures e as evidências de falhas |
| `tests/test_solicitacao_credito.py` | Testa os cenários de aprovação e reprovação |
| `tests/test_validacao_formulario.py` | Testa campos obrigatórios, entradas inválidas e limpeza do formulário |
| `requirements-app.txt` | Registra as dependências da aplicação |
| `requirements-dev.txt` | Registra as dependências necessárias para executar a suíte |
| `pytest.ini` | Configura a descoberta dos testes e a geração dos relatórios |
| `.github/workflows/testes-web.yml` | Define a execução dos testes no GitHub Actions |
| `.gitignore` | Exclui do versionamento ambientes locais, caches e relatórios |

## Arquitetura da automação

A automação utiliza o padrão Page Object para separar
os testes dos detalhes de interação com a interface.

### BasePage

Centraliza comportamentos compartilhados:

- Aguardar um elemento ficar visível.
- Preencher campos.
- Aguardar um elemento ficar disponível para clique.
- Clicar em elementos.

Utiliza `WebDriverWait` e condições esperadas do Selenium
para sincronizar as interações com a página.

### CreditoPage

Representa a página do simulador e concentra:

- Localizadores dos campos e botões.
- Preenchimento da solicitação.
- Envio da análise.
- Consulta do status e dos motivos de reprovação.
- Leitura das mensagens de validação.
- Verificação dos valores dos campos e do foco.
- Limpeza do formulário.

### Testes

Descrevem os cenários e verificam os resultados esperados,
utilizando os métodos disponibilizados pelos Page Objects.

### Fixtures

Preparam e encerram os recursos necessários:

- Uma aplicação local por sessão de testes.
- Uma sessão do Chrome por teste.
- Um Page Object com o simulador aberto.
- Capturas de tela quando há falhas de preparação ou execução,
  desde que o navegador esteja disponível.

## Aplicação demonstrativa independente

A aplicação necessária para os testes está dentro deste repositório,
na pasta `app`.

Por padrão, ao executar o pytest:

1. Uma porta local disponível é reservada.
2. O servidor da aplicação é iniciado.
3. A disponibilidade de `/health` e `/simulador` é verificada.
4. Os testes são executados no Chrome.
5. Cada sessão do navegador é encerrada após seu teste.
6. O servidor é encerrado ao final da sessão.

Não é necessário baixar ou iniciar o projeto
`qa-credito-api-python` para executar esta suíte.

## Regras de negócio

Todos os campos são obrigatórios:

- Idade.
- Renda mensal.
- Valor solicitado.

### Validação dos dados

- A idade deve ser um número inteiro entre 0 e 120.
- A renda mensal deve ser maior que zero.
- O valor solicitado deve ser maior que zero.
- Os valores monetários devem ter no máximo duas casas decimais.

### Critérios de aprovação

Uma solicitação será aprovada quando atender a todos os critérios:

- Idade igual ou superior a 18 anos.
- Renda mensal igual ou superior a R$ 2.000,00.
- Valor solicitado menor ou igual a cinco vezes a renda mensal.

Solicitações com dados válidos que não atendem aos critérios
recebem o resultado `REPROVADO`, com os respectivos motivos.

Dados inválidos geram mensagens de validação no formulário.

## Estratégia de testes

A suíte atual possui **24 testes web**:

| Grupo | Quantidade |
| --- | ---: |
| Aprovação e valores de fronteira | 2 |
| Reprovação por regras de negócio | 4 |
| Campos obrigatórios | 4 |
| Entradas inválidas | 10 |
| Separadores decimais | 2 |
| Limpeza do formulário | 2 |
| **Total** | **24** |

### Aprovação e valores de fronteira

- Aprovar uma solicitação com dados válidos.
- Aprovar uma solicitação com idade mínima, renda mínima
  e valor solicitado no limite permitido.

### Reprovação

- Reprovar solicitante menor de idade.
- Reprovar renda abaixo do mínimo.
- Reprovar valor solicitado acima do limite.
- Exibir todos os motivos quando vários critérios falham.

### Campos obrigatórios

- Exigir idade.
- Exigir renda mensal.
- Exigir valor solicitado.
- Exigir todos os campos quando o formulário estiver vazio.

As verificações incluem mensagens, indicação de campo inválido,
foco no primeiro campo com erro e ausência de resultado da análise.

### Entradas inválidas

- Idade negativa.
- Idade acima de 120.
- Idade fracionária.
- Idade preenchida com texto.
- Renda igual a zero.
- Renda com mais de duas casas decimais.
- Renda preenchida com texto.
- Valor solicitado igual a zero.
- Valor solicitado com mais de duas casas decimais.
- Valor solicitado preenchido com texto.

### Separadores decimais

- Aceitar valores monetários com vírgula.
- Aceitar valores monetários com ponto.

### Limpeza do formulário

- Limpar os campos e o resultado após uma análise.
- Limpar as mensagens e as indicações de validação.

## Pré-requisitos

- Python 3.13.
- Google Chrome instalado.
- Git, caso o projeto seja obtido por clonagem.
- Acesso à internet para instalar as dependências e,
  quando necessário, obter o driver do navegador.

A execução local foi validada com Python 3.13.5 no Windows.

Não é necessário instalar o ChromeDriver manualmente
na configuração padrão, pois o Selenium Manager gerencia
o driver quando necessário.

## Obter o projeto

```bash
git clone https://github.com/LeticiaGBrito/qa-credito-web-python.git
cd qa-credito-web-python
```

Execute os próximos comandos na raiz do projeto.

## Preparar o ambiente

### Windows PowerShell

Crie o ambiente virtual:

```powershell
py -3.13 -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### Linux ou macOS

Com Python 3.13 disponível:

```bash
python3.13 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
```

Não é necessário ativar o ambiente virtual quando seu executável
é utilizado explicitamente nos comandos.

## Executar todos os testes

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Linux ou macOS

```bash
./.venv/bin/python -m pytest
```

Por padrão, a aplicação é iniciada automaticamente e o Chrome
abre com interface visível e janela maximizada.

## Executar apenas parte da suíte

### Cenários de aprovação e reprovação

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_solicitacao_credito.py
```

### Validações do formulário

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_validacao_formulario.py
```

### Apenas cenários de aprovação

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_solicitacao_credito.py -k deve_aprovar
```

O resultado `deselected` indica que outros testes foram
excluídos pelo filtro utilizado; não significa falha.

## Executar sem abrir a janela do navegador

O modo headless executa o Chrome sem interface visível.

### Windows PowerShell

```powershell
$env:HEADLESS = "true"
.\.venv\Scripts\python.exe -m pytest
```

Para voltar à execução com janela visível:

```powershell
Remove-Item Env:HEADLESS -ErrorAction SilentlyContinue
```

### Linux ou macOS

```bash
HEADLESS=true ./.venv/bin/python -m pytest
```

No modo headless, a janela é configurada com
dimensões de 1440 × 1000 pixels.

## Configuração opcional de endereço externo

A variável `BASE_URL` permite testar outra instância compatível
da aplicação.

Quando essa variável está definida, a fixture utiliza o endereço
informado e não inicia nem encerra a aplicação externa.

Essa aplicação deve disponibilizar `/simulador`, os mesmos
elementos de interface e os comportamentos esperados pela suíte.

### Exemplo no Windows PowerShell

```powershell
$env:BASE_URL = "http://127.0.0.1:8000"
.\.venv\Scripts\python.exe -m pytest
```

Nesse modo, a aplicação externa precisa estar em execução.

Para voltar ao modo independente, com inicialização automática:

```powershell
Remove-Item Env:BASE_URL -ErrorAction SilentlyContinue
.\.venv\Scripts\python.exe -m pytest
```

## Relatórios e evidências

Os relatórios são gerados automaticamente conforme
a configuração do `pytest.ini`.

| Arquivo ou pasta | Finalidade |
| --- | --- |
| `reports/relatorio-testes.html` | Visualização dos resultados no navegador |
| `reports/resultados.xml` | Resultados em formato compatível com JUnit XML |
| `reports/screenshots/` | Capturas de tela geradas em caso de falha |

### Abrir o relatório no Windows

```powershell
Start-Process .\reports\relatorio-testes.html
```

O relatório HTML apresenta os resultados, a duração dos testes
e informações do ambiente de execução.

### Capturas de tela

Quando um teste falha durante a preparação ou execução
e o navegador está disponível:

- Uma captura é anexada ao relatório HTML.
- Uma cópia em PNG é salva em `reports/screenshots/`.

Se o navegador não estiver disponível, a captura não poderá
ser realizada.

A ausência de screenshots em uma execução sem falhas é esperada.

Os arquivos HTML e XML são sobrescritos a cada execução.
Capturas anteriores podem permanecer na pasta de screenshots.

Os relatórios e as capturas não são versionados no Git.

## Integração contínua com GitHub Actions

O workflow está definido em:

```text
.github/workflows/testes-web.yml
```

Ele pode ser executado:

- A cada push para a branch `main`.
- Em pull requests direcionados à branch `main`.
- Manualmente pela opção `Run workflow`, na aba Actions.

### Etapas da execução

1. Baixar o repositório.
2. Configurar Python 3.13.
3. Instalar as dependências.
4. Verificar a consistência das dependências com `pip check`.
5. Conferir a versão do Chrome.
6. Executar a suíte com `python -m pytest`.
7. Disponibilizar os relatórios e as evidências como artefato.

A execução utiliza Ubuntu 24.04 e Chrome em modo headless.

O próprio pytest inicia e encerra a aplicação demonstrativa.
O workflow não precisa baixar outro repositório nem iniciar
um servidor em uma etapa separada.

### Consultar os resultados

1. Abra a aba **Actions** do repositório.
2. Selecione a execução desejada.
3. Abra o job **Selenium com Chrome**.
4. Consulte a etapa **Executar os testes web**.

### Baixar os relatórios

Na página da execução, procure a seção **Artifacts** e baixe:

```text
relatorios-testes-web-python
```

Extraia o arquivo baixado antes de abrir o relatório HTML.

Os artefatos estão configurados para retenção de 14 dias.
A etapa de publicação dos relatórios é executada mesmo quando
uma etapa anterior falha, desde que existam arquivos para enviar.

Este workflow implementa integração contínua (CI).
Ele não publica nem implanta a aplicação em uma hospedagem.

## Executar o simulador manualmente

Esta etapa é opcional e não é necessária para executar os testes.

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.credito_api:app --host 127.0.0.1 --port 8000
```

### Linux ou macOS

```bash
./.venv/bin/python -m uvicorn app.credito_api:app --host 127.0.0.1 --port 8000
```

Com o servidor em execução, acesse:

- Simulador: http://127.0.0.1:8000/simulador
- Disponibilidade: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs

Para encerrar, pressione `Ctrl + C` no terminal.

## Limites do projeto

- Aplicação e regras de crédito educacionais.
- Sem autenticação ou persistência em banco de dados.
- Sem dados reais de clientes.
- Sem integração com serviços financeiros externos.
- A suíte atual utiliza apenas o Google Chrome.
- Não inclui testes de carga, segurança ou acessibilidade completos.
- Os tempos apresentados no relatório não representam
  resultados de testes de performance.
- Testes aprovados não significam ausência de defeitos
  ou cobertura total.
- O workflow deste repositório executa CI, sem deploy automático.

## Autora

Letícia Gonçalves Garcia — QA Sênior

[Portfólio](https://leticiagbrito.github.io/)

[GitHub](https://github.com/LeticiaGBrito)
