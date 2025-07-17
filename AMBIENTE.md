# Ambiente de Desenvolvimento - MCP Busca Município Validador

## Configuração do Ambiente

### 1. Ambiente Virtual Python

O projeto possui um ambiente virtual Python configurado na pasta `venv/`.

#### Para ativar o ambiente:

**Windows (CMD/PowerShell):**
```bash
# Opção 1: Usar o script batch
ativar_ambiente.bat

# Opção 2: Comando direto
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Para desativar o ambiente:
```bash
deactivate
```

### 2. Dependências

Este projeto utiliza apenas módulos padrão do Python 3, não requerendo instalação de pacotes externos.

**Módulos utilizados:**
- `os` - Operações do sistema operacional
- `sys` - Parâmetros e funções específicas do sistema
- `collections` (defaultdict) - Estruturas de dados especializadas
- `datetime` - Manipulação de datas e horas
- `unicodedata` - Normalização e manipulação de caracteres Unicode

**Versão Python recomendada:** Python 3.8 ou superior

### 3. Estrutura do Projeto

```
MCP-busca-municipio-validador/
├── venv/                              # Ambiente virtual Python
├── PresetFiles/                       # Arquivos de dados
│   ├── TACES06.TXT                   # Dados dos municípios
│   ├── TFIX105.txt                   # Dados dos validadores
│   └── tfixes.xml                    # Arquivo XML adicional
├── associar_municipios_validadores.py # Módulo de associação de dados
├── buscar_municipio_validador.py      # Script principal de busca
├── exemplo_uso.py                     # Exemplos de uso do sistema
├── requirements.txt                   # Dependências do projeto
├── ativar_ambiente.bat               # Script para ativar ambiente (Windows)
├── .gitignore                        # Arquivos ignorados pelo Git
├── AMBIENTE.md                       # Este arquivo
└── README.md                         # Documentação do projeto
```

### 4. Como Executar

1. **Ative o ambiente virtual:**
   ```bash
   ativar_ambiente.bat
   ```

2. **Execute o script principal:**
   ```bash
   # Buscar apenas município
   python buscar_municipio_validador.py "nome do município"
   
   # Buscar município e classificar validador
   python buscar_municipio_validador.py "nome do município" "nome do validador"
   ```

3. **Exemplos práticos:**
   ```bash
   python buscar_municipio_validador.py "rio de janeiro"
   python buscar_municipio_validador.py "sao paulo" "ISS DIGITAL"
   python buscar_municipio_validador.py jacarei betha
   ```

4. **Executar exemplos de uso:**
   ```bash
   python exemplo_uso.py
   ```

### 5. Arquivos Gerados

Durante a execução, o sistema pode gerar arquivos de saída:
- `municipios_validadores_*.txt` - Relatórios de associação município-validador
- Estes arquivos são ignorados pelo Git (conforme `.gitignore`)

### 6. Manutenção

- O ambiente virtual (`venv/`) não deve ser commitado no repositório
- Para recriar o ambiente em outro computador, execute:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  # ou
  source venv/bin/activate  # Linux/Mac
  ```

### 7. Desenvolvimento

Para contribuir com o projeto:
1. Ative o ambiente virtual
2. Faça suas alterações
3. Teste usando `exemplo_uso.py`
4. Commite apenas os arquivos fonte (não o `venv/`) 