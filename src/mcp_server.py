#!/usr/bin/env python3
"""
MCP Server para Busca de Município Validador
Fornece ferramentas para buscar e classificar validadores de municípios brasileiros
"""

from typing import Dict, List, Optional, Any
import json
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PATH para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    BlobResourceContents
)
from associar_municipios_validadores import AssociadorMunicipiosValidadores
from buscar_municipio_validador import remover_acentos
from datetime import datetime
import unicodedata

# Instância global do servidor
app = Server("mcp-busca-municipio-validador")

# Caminhos dos arquivos de dados
BASE_DIR = Path(__file__).parent.parent
ARQUIVO_MUNICIPIOS = BASE_DIR / "PresetFiles" / "TACES06.TXT"
ARQUIVO_VALIDADORES = BASE_DIR / "PresetFiles" / "TFIX105.txt"

# Cache dos dados carregados
_associador_cache = None

def get_associador():
    """Obtém ou cria uma instância do associador com cache"""
    global _associador_cache
    if _associador_cache is None:
        _associador_cache = AssociadorMunicipiosValidadores(
            str(ARQUIVO_MUNICIPIOS), 
            str(ARQUIVO_VALIDADORES)
        )
        _associador_cache.carregar_municipios()
        _associador_cache.carregar_validadores()
        _associador_cache.associar_dados()
    return _associador_cache

@app.list_tools()
async def list_tools() -> List[Tool]:
    """Lista as ferramentas disponíveis no servidor MCP"""
    return [
        Tool(
            name="buscar_municipio",
            description="Busca validadores de um município brasileiro específico",
            inputSchema={
                "type": "object",
                "properties": {
                    "nome_municipio": {
                        "type": "string",
                        "description": "Nome do município a buscar (aceita nomes parciais e ignora acentuação)"
                    }
                },
                "required": ["nome_municipio"]
            }
        ),
        Tool(
            name="classificar_validador",
            description="Classifica a implementação de um validador para um município específico",
            inputSchema={
                "type": "object",
                "properties": {
                    "nome_municipio": {
                        "type": "string",
                        "description": "Nome do município"
                    },
                    "nome_validador": {
                        "type": "string",
                        "description": "Nome do validador a classificar"
                    }
                },
                "required": ["nome_municipio", "nome_validador"]
            }
        ),
        Tool(
            name="listar_validadores",
            description="Lista todos os validadores únicos cadastrados no sistema",
            inputSchema={
                "type": "object",
                "properties": {
                    "filtro_estado": {
                        "type": "string",
                        "description": "Código do estado para filtrar (opcional, ex: SP, RJ)"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Executa uma ferramenta específica"""
    
    if name == "buscar_municipio":
        resultado = buscar_municipio_tool(arguments.get("nome_municipio"))
        return [TextContent(type="text", text=resultado)]
    
    elif name == "classificar_validador":
        resultado = classificar_validador_tool(
            arguments.get("nome_municipio"),
            arguments.get("nome_validador")
        )
        return [TextContent(type="text", text=resultado)]
    
    elif name == "listar_validadores":
        resultado = listar_validadores_tool(arguments.get("filtro_estado"))
        return [TextContent(type="text", text=resultado)]
    
    else:
        return [TextContent(type="text", text=f"Ferramenta '{name}' não encontrada")]

def buscar_municipio_tool(nome_municipio: str) -> str:
    """Busca validadores de um município"""
    if not nome_municipio:
        return "Nome do município é obrigatório"
    
    associador = get_associador()
    
    # Busca o município
    municipios_encontrados = []
    municipios_parciais = []
    nome_busca = remover_acentos(nome_municipio.upper().strip())
    
    # Busca exata primeiro
    for registro in associador.resultados:
        nome_registro = remover_acentos(registro['descricao'].upper().strip())
        
        if nome_busca == nome_registro:
            municipios_encontrados.append(registro)
        elif nome_busca in nome_registro:
            municipios_parciais.append(registro)
    
    # Se não encontrou exata, usa parciais
    if not municipios_encontrados and municipios_parciais:
        municipios_encontrados = municipios_parciais
    
    if not municipios_encontrados:
        # Sugere similares
        similares = []
        palavras_busca = nome_busca.split()
        
        for registro in associador.resultados:
            nome_registro = remover_acentos(registro['descricao'].upper())
            for palavra in palavras_busca:
                if len(palavra) >= 3 and palavra in nome_registro:
                    if registro not in similares:
                        similares.append(registro)
                        break
        
        # Remove duplicatas
        municipios_unicos = {}
        for s in similares:
            chave = f"{s['descricao']} ({s['cod_estado']})"
            municipios_unicos[chave] = s
        
        resultado = f"Município '{nome_municipio}' não encontrado!\n\n"
        resultado += "Municípios similares:\n"
        for nome in sorted(municipios_unicos.keys())[:20]:
            resultado += f"  - {nome}\n"
        
        return resultado
    
    # Remove duplicatas
    municipios_unicos = {}
    for m in municipios_encontrados:
        chave = (m['cod_estado'], m['cod_municipio'], m['cod_validador'])
        municipios_unicos[chave] = m
    
    municipios_encontrados = list(municipios_unicos.values())
    
    # Separa por município
    municipios_por_codigo = {}
    for registro in municipios_encontrados:
        chave = (registro['cod_estado'], registro['cod_municipio'])
        if chave not in municipios_por_codigo:
            municipios_por_codigo[chave] = {
                'info': {
                    'estado': registro['cod_estado'],
                    'codigo': registro['cod_municipio'],
                    'nome': registro['descricao']
                },
                'validadores': []
            }
        if registro['cod_validador']:
            municipios_por_codigo[chave]['validadores'].append(registro)
    
    # Formata resultado
    resultado = ""
    for chave, dados in municipios_por_codigo.items():
        info = dados['info']
        validadores = dados['validadores']
        
        resultado += f"\nMUNICÍPIO: {info['nome']} - {info['estado']} (Código: {info['codigo']})\n"
        resultado += "=" * 80 + "\n\n"
        
        if not validadores:
            resultado += "❌ Este município NÃO possui validadores cadastrados.\n"
        else:
            resultado += "📋 VALIDADORES DO MUNICÍPIO:\n\n"
            resultado += f"{'VALIDADOR':25} | {'DESCRIÇÃO':35} | {'DT INICIAL':10} | {'DT VALID':10} | {'STATUS':10}\n"
            resultado += "-" * 100 + "\n"
            
            for v in validadores:
                data_inicial = v.get('data_inicial', '')
                
                # Verifica status
                if not v['valid_validador']:
                    situacao = "ATIVO"
                else:
                    try:
                        dia, mes, ano = v['valid_validador'].split('/')
                        data_valid = datetime(int(ano), int(mes), int(dia))
                        if data_valid < datetime.now():
                            situacao = "EXPIRADO"
                        else:
                            situacao = "ATIVO"
                    except:
                        situacao = "ATIVO"
                
                status = f"{v['valid_final']}-{situacao}"
                
                resultado += f"{v['cod_validador'][:25]:25} | "
                resultado += f"{v['desc_validador'][:35]:35} | "
                resultado += f"{data_inicial:^10} | "
                resultado += f"{v['valid_validador']:^10} | "
                resultado += f"{status:10}\n"
    
    return resultado

def classificar_validador_tool(nome_municipio: str, nome_validador: str) -> str:
    """Classifica um validador para um município"""
    if not nome_municipio or not nome_validador:
        return "Nome do município e validador são obrigatórios"
    
    # Primeiro busca o município
    resultado_busca = buscar_municipio_tool(nome_municipio)
    
    if "não encontrado" in resultado_busca:
        return resultado_busca
    
    associador = get_associador()
    
    # Busca o município novamente para classificar
    municipios_encontrados = []
    nome_busca = remover_acentos(nome_municipio.upper().strip())
    
    for registro in associador.resultados:
        nome_registro = remover_acentos(registro['descricao'].upper().strip())
        if nome_busca == nome_registro or nome_busca in nome_registro:
            municipios_encontrados.append(registro)
    
    if not municipios_encontrados:
        return f"Município '{nome_municipio}' não encontrado"
    
    # Verifica se o validador existe no sistema
    validador_existe_geral = False
    for municipio_validadores in associador.validadores.values():
        for v in municipio_validadores:
            if (nome_validador.upper() in v['cod_validador'].upper() or 
                nome_validador.upper() in v['desc_validador'].upper()):
                validador_existe_geral = True
                break
        if validador_existe_geral:
            break
    
    resultado = resultado_busca + "\n\n"
    resultado += f"📋 CLASSIFICAÇÃO DO VALIDADOR '{nome_validador}':\n\n"
    
    if not validador_existe_geral:
        resultado += "✅ NOVO VALIDADOR\n"
        resultado += "→ Este validador não existe no sistema\n"
    else:
        # Verifica se o município usa este validador
        validador_existe_municipio = False
        validador_atual = None
        
        for registro in municipios_encontrados:
            if registro['cod_validador']:
                if (nome_validador.upper() in registro['cod_validador'].upper() or 
                    nome_validador.upper() in registro['desc_validador'].upper()):
                    validador_existe_municipio = True
                    
                # Identifica o validador atual
                if registro['valid_final'] == 'S' and not registro['valid_validador']:
                    validador_atual = registro
        
        if not validador_existe_municipio:
            resultado += "↔️ MIGRAÇÃO DE VALIDADOR\n"
            resultado += f"→ O validador existe no sistema mas nunca foi usado por {municipios_encontrados[0]['descricao']}\n"
        elif validador_atual and (nome_validador.upper() in validador_atual['cod_validador'].upper() or 
                                 nome_validador.upper() in validador_atual['desc_validador'].upper()):
            resultado += "🔄 ALTERAÇÃO DE REGRAS\n"
            resultado += f"→ {municipios_encontrados[0]['descricao']} já usa este validador atualmente\n"
        else:
            resultado += "↔️ MIGRAÇÃO DE VALIDADOR\n"
            resultado += f"→ {municipios_encontrados[0]['descricao']} já usou este validador, mas não é o atual\n"
            if validador_atual:
                resultado += f"→ Mudança de '{validador_atual['desc_validador']}' para '{nome_validador}'\n"
    
    return resultado

def listar_validadores_tool(filtro_estado: Optional[str] = None) -> str:
    """Lista todos os validadores únicos do sistema"""
    associador = get_associador()
    
    validadores_unicos = {}
    
    for estado_municipio, validadores in associador.validadores.items():
        estado = estado_municipio[0]
        
        # Aplica filtro de estado se fornecido
        if filtro_estado and estado != filtro_estado.upper():
            continue
            
        for v in validadores:
            chave = v['cod_validador']
            if chave not in validadores_unicos:
                validadores_unicos[chave] = {
                    'codigo': v['cod_validador'],
                    'descricao': v['desc_validador'],
                    'estados': set(),
                    'municipios': 0
                }
            validadores_unicos[chave]['estados'].add(estado)
            validadores_unicos[chave]['municipios'] += 1
    
    # Formata resultado
    resultado = "VALIDADORES CADASTRADOS NO SISTEMA\n"
    if filtro_estado:
        resultado += f"Filtrado por estado: {filtro_estado.upper()}\n"
    resultado += "=" * 80 + "\n\n"
    
    resultado += f"{'CÓDIGO':25} | {'DESCRIÇÃO':35} | {'ESTADOS':10} | {'MUNICÍPIOS':10}\n"
    resultado += "-" * 85 + "\n"
    
    for v in sorted(validadores_unicos.values(), key=lambda x: x['municipios'], reverse=True):
        estados_str = ','.join(sorted(v['estados']))[:10]
        resultado += f"{v['codigo'][:25]:25} | "
        resultado += f"{v['descricao'][:35]:35} | "
        resultado += f"{estados_str:10} | "
        resultado += f"{v['municipios']:10}\n"
    
    resultado += f"\nTotal de validadores únicos: {len(validadores_unicos)}\n"
    
    return resultado

def main():
    """Função principal para executar o servidor MCP"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream)
    
    asyncio.run(run())

if __name__ == "__main__":
    main() 