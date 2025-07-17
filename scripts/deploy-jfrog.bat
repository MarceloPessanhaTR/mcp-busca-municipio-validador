@echo off
REM Script para deploy no JFrog Artifactory - Windows

REM Variáveis de configuração
if "%JFROG_URL%"=="" set JFROG_URL=https://seu-jfrog.jfrog.io/artifactory/api/pypi/pypi-local
if "%JFROG_USER%"=="" set JFROG_USER=seu-usuario

echo 🚀 Deploy para JFrog Artifactory
echo ================================

REM Verifica se as variáveis estão configuradas
if "%JFROG_TOKEN%"=="" (
    echo ❌ Erro: JFROG_TOKEN não está configurado!
    echo    Configure com: set JFROG_TOKEN=seu-token-aqui
    exit /b 1
)

REM Verifica se existe o diretório dist
if not exist dist (
    echo ❌ Erro: Diretório dist não encontrado!
    echo    Execute scripts\build.bat primeiro
    exit /b 1
)

REM Instala twine se necessário
echo 📦 Verificando twine...
python -m pip install --upgrade twine

REM Upload para o JFrog usando twine diretamente
echo 📤 Enviando pacotes para JFrog...
python -m twine upload --repository-url %JFROG_URL% -u %JFROG_USER% -p %JFROG_TOKEN% dist/*

if %errorlevel% equ 0 (
    echo ✅ Deploy concluído com sucesso!
    echo 📦 Pacote disponível em: %JFROG_URL%
    echo.
    echo Para instalar via uvx:
    echo   uvx install mcp-busca-municipio-validador --index-url %JFROG_URL%
) else (
    echo ❌ Erro durante o deploy!
    exit /b 1
) 