@echo off
echo ======================================
echo Ativando ambiente virtual do projeto
echo MCP-busca-municipio-validador
echo ======================================
echo.
call venv\Scripts\activate
echo.
echo Ambiente ativado com sucesso!
echo.
echo Para executar o projeto, use:
echo   python buscar_municipio_validador.py [nome_municipio] [nome_validador]
echo.
echo Exemplos:
echo   python buscar_municipio_validador.py "rio de janeiro"
echo   python buscar_municipio_validador.py "sao paulo" "ISS DIGITAL"
echo   python buscar_municipio_validador.py jacarei betha
echo.
echo Para desativar o ambiente, use: deactivate
echo. 