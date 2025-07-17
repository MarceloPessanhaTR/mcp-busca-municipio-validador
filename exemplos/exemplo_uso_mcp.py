#!/usr/bin/env python3
"""
Exemplo de uso do MCP Busca Município Validador
Este exemplo mostra como usar o servidor MCP programaticamente
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def exemplo_uso_mcp():
    """Demonstra o uso das ferramentas do MCP"""
    
    # Configura o servidor
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.mcp_server"]
    )
    
    # Conecta ao servidor
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializa a sessão
            await session.initialize()
            
            print("🚀 MCP Busca Município Validador - Exemplo de Uso")
            print("="*60)
            
            # Lista as ferramentas disponíveis
            tools = await session.list_tools()
            print("\n📋 Ferramentas disponíveis:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Exemplo 1: Buscar município
            print("\n\n1️⃣ Buscando validadores de São Paulo...")
            result1 = await session.call_tool(
                "buscar_municipio",
                {"nome_municipio": "São Paulo"}
            )
            print(result1.content[0].text)
            
            # Exemplo 2: Classificar validador
            print("\n\n2️⃣ Classificando validador ISS DIGITAL para Jacareí...")
            result2 = await session.call_tool(
                "classificar_validador",
                {
                    "nome_municipio": "Jacareí",
                    "nome_validador": "ISS DIGITAL"
                }
            )
            print(result2.content[0].text)
            
            # Exemplo 3: Listar validadores
            print("\n\n3️⃣ Listando validadores do estado SP...")
            result3 = await session.call_tool(
                "listar_validadores",
                {"filtro_estado": "SP"}
            )
            print(result3.content[0].text[:500] + "...")  # Mostra apenas início
            
            # Exemplo 4: Buscar município inexistente
            print("\n\n4️⃣ Buscando município inexistente...")
            result4 = await session.call_tool(
                "buscar_municipio",
                {"nome_municipio": "Cidade Imaginária"}
            )
            print(result4.content[0].text)

async def exemplo_busca_avancada():
    """Exemplo de busca avançada com múltiplos municípios"""
    
    municipios_teste = [
        "Rio de Janeiro",
        "Belo Horizonte",
        "Porto Alegre",
        "Curitiba",
        "Salvador"
    ]
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.mcp_server"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n🔍 Busca Avançada - Validadores de Capitais")
            print("="*60)
            
            for municipio in municipios_teste:
                print(f"\n📍 {municipio}:")
                result = await session.call_tool(
                    "buscar_municipio",
                    {"nome_municipio": municipio}
                )
                
                # Extrai apenas o resumo
                texto = result.content[0].text
                if "VALIDADORES DO MUNICÍPIO:" in texto:
                    # Mostra apenas a primeira linha de validadores
                    linhas = texto.split('\n')
                    for i, linha in enumerate(linhas):
                        if "VALIDADORES DO MUNICÍPIO:" in linha:
                            print(f"  {linhas[i+3] if i+3 < len(linhas) else 'Sem validadores'}")
                            break
                else:
                    print("  ❌ Sem validadores cadastrados")

def main():
    """Função principal"""
    print("🎯 Exemplos de uso do MCP Busca Município Validador\n")
    
    # Executa o exemplo básico
    asyncio.run(exemplo_uso_mcp())
    
    # Executa o exemplo avançado
    asyncio.run(exemplo_busca_avancada())

if __name__ == "__main__":
    main() 