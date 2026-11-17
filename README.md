# EcoMode

Uma ferramenta de linha de comando pequena para reduzir texto desnecessário antes de enviar logs ou saídas de terminal a agentes de IA. O EcoMode remove linhas normais repetidas, limita a quantidade de linhas normais únicas e mantém mensagens de erro e aviso.

O projeto usa apenas a biblioteca padrão do Python durante a execução. Ele não mede nem promete uma porcentagem específica de economia: o resultado depende da saída processada.

## Português

### Requisitos

- Python 3.9 ou mais recente
- Windows PowerShell, Prompt de Comando ou outro terminal compatível

### Instalação no Windows

Baixe ou clone o repositório e, dentro da pasta do projeto, execute:

```powershell
python -m pip install --user .
```

Se o comando `ecomode` não for encontrado depois da instalação, feche e reabra o terminal. Você também pode usar o script diretamente, sem instalar:

```powershell
python .\ecomode.py --help
```

### Uso

Processar um arquivo:

```powershell
ecomode .\saida.txt
```

Processar a saída de outro comando e manter no máximo 100 linhas normais únicas:

```powershell
seu-comando 2>&1 | ecomode --max-lines 100
```

Erros e avisos reconhecidos são preservados mesmo quando aparecem depois do limite. O resumo final informa quantas linhas repetidas ou excedentes foram omitidas.

### Uso local no Codex

1. Instale o EcoMode na máquina ou mantenha `ecomode.py` em um caminho conhecido.
2. Copie as orientações de `AGENTS.md` para o projeto em que deseja usar o EcoMode, ou adapte o `AGENTS.md` existente.
3. Em comandos com muita saída, peça ao Codex para usar `comando 2>&1 | ecomode` quando o filtro não remover contexto necessário.

Essa instalação disponibiliza uma ferramenta local e instruções para projetos que adotarem o arquivo `AGENTS.md`. Ela **não altera automaticamente todas as conversas do ChatGPT Work**, nem intercepta mensagens ou comandos globalmente.

### Desinstalação

Se instalou com `pip`:

```powershell
python -m pip uninstall ecomode-ai
```

Depois, exclua a pasta clonada se não precisar mais dela. Em outros projetos, remova apenas as instruções do EcoMode que você copiou para os respectivos arquivos `AGENTS.md`.

### Testes

```powershell
python -m unittest discover -s tests -v
```

## English

EcoMode is a small command-line tool that reduces unnecessary text before terminal output or logs are sent to AI agents. It removes repeated normal lines, caps unique normal lines, and keeps recognized errors and warnings.

It uses only the Python standard library at runtime. It does not measure or promise a specific savings percentage; results depend on the input.

### Requirements

- Python 3.9 or newer
- Windows PowerShell, Command Prompt, or another compatible terminal

### Install on Windows

Download or clone the repository, open its directory, and run:

```powershell
python -m pip install --user .
```

If `ecomode` is not found afterward, close and reopen the terminal. You can also run it without installing:

```powershell
python .\ecomode.py --help
```

### Usage

Process a file:

```powershell
ecomode .\output.txt
```

Process another command's output and keep at most 100 unique normal lines:

```powershell
your-command 2>&1 | ecomode --max-lines 100
```

Recognized errors and warnings are preserved even after the limit. A final summary reports how many duplicate or excess lines were omitted.

### Local use with Codex

1. Install EcoMode locally, or keep `ecomode.py` at a known path.
2. Copy the guidance from `AGENTS.md` into the project where you want to use EcoMode, or adapt that project's existing `AGENTS.md`.
3. For verbose commands, ask Codex to use `command 2>&1 | ecomode` when filtering will not hide required context.

This makes a local tool and project instructions available where you adopt them. It **does not automatically change every ChatGPT Work conversation**, and it does not globally intercept messages or commands.

### Uninstall

If installed with `pip`:

```powershell
python -m pip uninstall ecomode-ai
```

Then delete the cloned directory if it is no longer needed. In other projects, remove only the EcoMode guidance you copied into their `AGENTS.md` files.

### Tests

```powershell
python -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
