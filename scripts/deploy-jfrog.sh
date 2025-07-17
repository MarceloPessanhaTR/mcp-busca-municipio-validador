#!/bin/bash
# Script para deploy no JFrog Artifactory

# Variáveis de configuração
JFROG_URL="${JFROG_URL:-https://seu-jfrog.jfrog.io/artifactory/api/pypi/pypi-local}"
JFROG_USER="${JFROG_USER:-seu-usuario}"
JFROG_TOKEN="${JFROG_TOKEN:-}"

echo "🚀 Deploy para JFrog Artifactory"
echo "================================"

# Verifica se as variáveis estão configuradas
if [ -z "$JFROG_TOKEN" ]; then
    echo "❌ Erro: JFROG_TOKEN não está configurado!"
    echo "   Configure com: export JFROG_TOKEN='seu-token-aqui'"
    exit 1
fi

# Verifica se existe o diretório dist
if [ ! -d "dist" ]; then
    echo "❌ Erro: Diretório dist não encontrado!"
    echo "   Execute ./scripts/build.sh primeiro"
    exit 1
fi

# Instala twine se necessário
echo "📦 Verificando twine..."
pip install --upgrade twine

# Configura o .pypirc temporário
echo "🔐 Configurando credenciais..."
cat > ~/.pypirc.tmp << EOF
[distutils]
index-servers =
    jfrog

[jfrog]
repository: $JFROG_URL
username: $JFROG_USER
password: $JFROG_TOKEN
EOF

# Upload para o JFrog
echo "📤 Enviando pacotes para JFrog..."
twine upload --config-file ~/.pypirc.tmp -r jfrog dist/*

# Limpa arquivo temporário
rm -f ~/.pypirc.tmp

if [ $? -eq 0 ]; then
    echo "✅ Deploy concluído com sucesso!"
    echo "📦 Pacote disponível em: $JFROG_URL"
    echo ""
    echo "Para instalar via uvx:"
    echo "  uvx install mcp-busca-municipio-validador --index-url $JFROG_URL"
else
    echo "❌ Erro durante o deploy!"
    exit 1
fi 