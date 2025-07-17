#!/bin/bash
# Script para build do MCP Busca Município Validador

echo "🚀 Iniciando build do MCP Busca Município Validador..."

# Limpa builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf dist/ build/ *.egg-info

# Instala dependências de build
echo "📦 Instalando dependências de build..."
pip install --upgrade pip build hatch

# Executa o build
echo "🔨 Construindo o pacote..."
python -m build

# Verifica se o build foi bem sucedido
if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    echo "📁 Arquivos gerados em ./dist/"
    ls -la dist/
else
    echo "❌ Erro durante o build!"
    exit 1
fi 