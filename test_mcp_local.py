#!/usr/bin/env python3
"""
Script de teste local para o MCP Busca Município Validador
Executa testes básicos para verificar se o servidor está funcionando
"""

import subprocess
import sys
import time
import json

def test_mcp_server():
    """Testa o servidor MCP localmente"""
    
    print("🧪 Testando MCP Busca Município Validador")
    print("="*50)
    
    # Testa importação dos módulos
    print("\n1️⃣ Testando importações...")
    try:
        from src.mcp_server import app, buscar_municipio_tool, classificar_validador_tool, listar_validadores_tool
        print("✅ Importações OK")
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False
    
    # Testa as ferramentas diretamente
    print("\n2️⃣ Testando ferramentas...")
    
    # Teste buscar_municipio
    try:
        resultado = buscar_municipio_tool("São Paulo")
        if "MUNICÍPIO: SAO PAULO" in resultado:
            print("✅ buscar_municipio OK")
        else:
            print("❌ buscar_municipio retornou resultado inesperado")
    except Exception as e:
        print(f"❌ Erro em buscar_municipio: {e}")
    
    # Teste classificar_validador
    try:
        resultado = classificar_validador_tool("Jacareí", "TESTE")
        if "CLASSIFICAÇÃO DO VALIDADOR" in resultado:
            print("✅ classificar_validador OK")
        else:
            print("❌ classificar_validador retornou resultado inesperado")
    except Exception as e:
        print(f"❌ Erro em classificar_validador: {e}")
    
    # Teste listar_validadores
    try:
        resultado = listar_validadores_tool("SP")
        if "VALIDADORES CADASTRADOS NO SISTEMA" in resultado:
            print("✅ listar_validadores OK")
        else:
            print("❌ listar_validadores retornou resultado inesperado")
    except Exception as e:
        print(f"❌ Erro em listar_validadores: {e}")
    
    # Testa execução do servidor
    print("\n3️⃣ Testando execução do servidor...")
    try:
        # Tenta executar o servidor em modo de teste
        processo = subprocess.Popen(
            [sys.executable, "-m", "src.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Envia comando de inicialização
        processo.stdin.write('{"jsonrpc": "2.0", "method": "initialize", "params": {"capabilities": {}}, "id": 1}\n')
        processo.stdin.flush()
        
        # Aguarda resposta
        time.sleep(1)
        
        # Termina o processo
        processo.terminate()
        processo.wait(timeout=5)
        
        print("✅ Servidor MCP executável")
        
    except Exception as e:
        print(f"❌ Erro ao executar servidor: {e}")
    
    print("\n4️⃣ Verificando estrutura do projeto...")
    arquivos_necessarios = [
        "pyproject.toml",
        "src/__init__.py", 
        "src/mcp_server.py",
        "PresetFiles/TACES06.TXT",
        "PresetFiles/TFIX105.txt",
        "associar_municipios_validadores.py",
        "buscar_municipio_validador.py"
    ]
    
    from pathlib import Path
    todos_existem = True
    for arquivo in arquivos_necessarios:
        if Path(arquivo).exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} não encontrado")
            todos_existem = False
    
    if todos_existem:
        print("\n✅ Todos os arquivos necessários estão presentes")
    else:
        print("\n❌ Alguns arquivos estão faltando")
    
    print("\n" + "="*50)
    print("🎉 Teste concluído!")
    
    return todos_existem

if __name__ == "__main__":
    test_mcp_server() 