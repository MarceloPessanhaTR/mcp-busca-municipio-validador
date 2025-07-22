# MCP Busca Município Validador

## 🎯 Visão Geral

Este é um servidor MCP (Model Context Protocol) que fornece ferramentas para buscar e classificar validadores de municípios brasileiros. O servidor expõe três ferramentas principais que podem ser usadas por assistentes de IA para consultar informações sobre validadores municipais.

## 📦 Instalação

### Via uvx (Recomendado)

```bash
# Instalação direta do PyPI
uvx install mcp-busca-municipio-validador

# Instalação do JFrog Artifactory
uvx install mcp-busca-municipio-validador --index-url https://tr1.jfrog.io/artifactory/pypi-local/taxone/mcp/mcp-busca_municipio_validador/simple
```

### Via pip

```bash
# Instalação direta
pip install mcp-busca-municipio-validador

# Instalação do JFrog
pip install mcp-busca-municipio-validador --index-url https://tr1.jfrog.io/artifactory/pypi-local/taxone/mcp/mcp-busca_municipio_validador/simple
```

## 🚀 Uso

### Execução do Servidor

```bash
# Via uvx
uvx run mcp-busca-municipio-validador

# Via Python
python -m src.mcp_server

# Ou diretamente
mcp-busca-municipio-validador
```

### Configuração no Claude Desktop

Adicione ao seu arquivo de configuração do Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "busca-municipio-validador": {
      "command": "uvx",
      "args": ["run", "mcp-busca-municipio-validador"]
    }
  }
}
```

Ou se instalado via pip:

```json
{
  "mcpServers": {
    "busca-municipio-validador": {
      "command": "mcp-busca-municipio-validador"
    }
  }
}
```

### Configuração no Cursor

Adicione ao seu arquivo de configuração do Cursor (`.cursor/mcp_config.json`):

```json
{
  "mcpServers": {
    "busca-municipio-validador": {
      "command": "uvx",
      "args": [
        "--index-url",
        "https://tr1.jfrog.io/artifactory/pypi-local/taxone/mcp/mcp-busca_municipio_validador/simple",
        "run",
        "mcp-busca-municipio-validador"
      ]
    }
  }
}
```

Ou se instalado localmente via pip:

```json
{
  "mcpServers": {
    "busca-municipio-validador": {
      "command": "python",
      "args": ["-m", "src.mcp_server"]
    }
  }
}
```

Ou se instalado globalmente:

```json
{
  "mcpServers": {
    "busca-municipio-validador": {
      "command": "mcp-busca-municipio-validador"
    }
  }
}
```

**Nota**: O Cursor procura o arquivo de configuração MCP em:
- Windows: `%USERPROFILE%\.cursor\mcp_config.json`
- macOS/Linux: `~/.cursor/mcp_config.json`

## 🛠️ Ferramentas Disponíveis

### 1. buscar_municipio

Busca validadores de um município brasileiro específico.

**Parâmetros:**
- `nome_municipio` (string, obrigatório): Nome do município a buscar

**Exemplo de uso:**
```
buscar_municipio("São Paulo")
buscar_municipio("rio de janeiro")
buscar_municipio("belo horizonte")
```

### 2. classificar_validador

Classifica a implementação de um validador para um município específico.

**Parâmetros:**
- `nome_municipio` (string, obrigatório): Nome do município
- `nome_validador` (string, obrigatório): Nome do validador a classificar

**Classificações possíveis:**
- ✅ **NOVO VALIDADOR**: Validador não existe no sistema
- ↔️ **MIGRAÇÃO DE VALIDADOR**: Validador existe mas município nunca usou ou não é o atual
- 🔄 **ALTERAÇÃO DE REGRAS**: Município já usa este validador atualmente

**Exemplo de uso:**
```
classificar_validador("Jacareí", "SIAP.NET")
classificar_validador("São Paulo", "ISS DIGITAL")
```

### 3. listar_validadores

Lista todos os validadores únicos cadastrados no sistema.

**Parâmetros:**
- `filtro_estado` (string, opcional): Código do estado para filtrar (ex: SP, RJ)

**Exemplo de uso:**
```
listar_validadores()
listar_validadores("SP")
listar_validadores("RJ")
```

## 📊 Estrutura dos Dados

O MCP utiliza dois arquivos de dados principais:

- **TACES06.TXT**: Lista de 5.569 municípios brasileiros
- **TFIX105.txt**: Lista de 776 registros de validadores

## 🔧 Build e Deploy

### Build Local

```bash
# Windows
scripts\build.bat

# Linux/Mac
./scripts/build.sh
```

### Deploy para JFrog

```bash
# Configurar credenciais
export JFROG_URL="https://tr1.jfrog.io/artifactory/pypi-local/taxone/mcp/mcp-busca_municipio_validador"
export JFROG_USER="seu-usuario"
export JFROG_TOKEN="seu-token"

# Windows
scripts\deploy-jfrog.bat

# Linux/Mac
./scripts/deploy-jfrog.sh
```

## 🐛 Troubleshooting

### Erro: "Município não encontrado"
- O sistema aceita nomes parciais e ignora acentuação
- Tente variações do nome ou parte do nome

### Erro de conexão com JFrog
- Verifique suas credenciais
- Confirme a URL do repositório
- Verifique se tem permissão de escrita

### Dados desatualizados
- Os dados são de 2015-2020 aproximadamente
- Alguns validadores podem estar expirados

## 📝 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request 