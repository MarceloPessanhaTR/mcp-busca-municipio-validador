@echo off
REM Script para build do MCP Busca Município Validador no Windows

echo 🚀 Iniciando build do MCP Busca Município Validador...

REM Limpa builds anteriores
echo 🧹 Limpando builds anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Instala dependências de build
echo 📦 Instalando dependências de build...
python -m pip install --upgrade pip build hatch

REM Executa o build
echo 🔨 Construindo o pacote...
python -m build

REM Verifica se o build foi bem sucedido
if %errorlevel% equ 0 (
    echo ✅ Build concluído com sucesso!
    echo 📁 Arquivos gerados em ./dist/
    dir dist
) else (
    echo ❌ Erro durante o build!
    exit /b 1
) 