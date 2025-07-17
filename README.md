# MCP-busca-municipio-validador

Sistema para busca e classificação de validadores de municípios brasileiros.

## 📋 Descrição

Este projeto permite:
- Buscar validadores de um município específico
- Classificar a implementação de um novo validador
- Identificar o histórico de validadores de um município

## 🚀 Como usar

### Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>

# Entre no diretório
cd MCP-busca-municipio-validador

# Não há dependências externas - usa apenas bibliotecas padrão do Python
```

### Uso básico

```bash
# Buscar validadores de um município
python buscar_municipio_validador.py "nome do municipio"

# Buscar e classificar um validador específico
python buscar_municipio_validador.py "nome do municipio" "nome do validador"

# Exemplos
python buscar_municipio_validador.py "rio de janeiro" "DIEF"
python buscar_municipio_validador.py "sao paulo" "BETHA"
python buscar_municipio_validador.py "nova iguacu"
```

## 📁 Estrutura de Arquivos

```
MCP-busca-municipio-validador/
│
├── buscar_municipio_validador.py    # Script principal
├── associar_municipios_validadores.py # Classe para associar dados
├── requirements.txt                  # Dependências (vazio - usa apenas libs padrão)
├── README.md                        # Este arquivo
│
└── PresetFiles/                     # Dados de entrada
    ├── TACES06.TXT                  # Lista de municípios (5.569 registros)
    └── TFIX105.txt                  # Lista de validadores (776 registros)
```

## 🎯 Classificações de Validadores

O sistema classifica validadores em 3 categorias:

### ✅ NOVO VALIDADOR
- Quando o validador não existe no sistema

### ↔️ MIGRAÇÃO DE VALIDADOR
- Quando o validador existe mas nunca foi usado pelo município
- Quando o validador já foi usado pelo município mas não é o atual

### 🔄 ALTERAÇÃO DE REGRAS
- Quando o validador é o mesmo que o município já usa atualmente

## 📊 Formato dos Dados

### TACES06.TXT (Municípios)
```
UF | Código | Nome | ... | Nome com acentuação
AC | 13     | ACRELANDIA | ... | Acrelândia
```

### TFIX105.txt (Validadores)
```
UF | CódMun | CódValidador | Descrição | DataInicial | ... | DataValidade
AL | 300    | EISSXML      | EISSXML   | 20150401    | ... | 20201207
```

## 🔍 Funcionalidades

1. **Busca flexível**: Aceita nomes parciais e ignora acentuação
2. **Múltiplos municípios**: Trata municípios com mesmo nome em estados diferentes
3. **Histórico**: Mostra todos os validadores já usados pelo município
4. **Data de validade**: Identifica validadores expirados
5. **Sugestões**: Sugere municípios similares quando não encontra exato

## 💡 Exemplos de Uso

### Buscar município sem especificar validador
```bash
python buscar_municipio_validador.py "belo horizonte"
```
Mostra todos os validadores do município.

### Classificar novo validador
```bash
python buscar_municipio_validador.py "jacarei" "SIAP.NET"
```
Informa se seria uma migração, alteração ou novo validador.

### Município com nome composto
```bash
python buscar_municipio_validador.py "sao jose dos campos" "ISS.NET"
```

## ⚠️ Observações

- Os dados são de 2015-2020 aproximadamente
- Alguns validadores podem estar expirados
- Municípios podem ter múltiplos validadores ativos
- A busca é case-insensitive e ignora acentos

## 📝 Licença

[Defina sua licença aqui]

## 👤 Autor

[Seu nome aqui] 