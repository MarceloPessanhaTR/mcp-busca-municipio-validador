#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplos de uso do sistema de busca de municípios e validadores
"""

from buscar_municipio_validador import buscar_municipio

def main():
    """Demonstra diferentes casos de uso do sistema"""
    
    print("="*80)
    print("EXEMPLOS DE USO DO SISTEMA DE BUSCA DE MUNICÍPIOS E VALIDADORES")
    print("="*80)
    
    # Exemplo 1: Buscar apenas município (sem validador)
    print("\n\n1. BUSCAR MUNICÍPIO SEM ESPECIFICAR VALIDADOR:")
    print("-"*80)
    buscar_municipio("rio de janeiro")
    
    # Exemplo 2: Município + Validador Atual (Alteração de Regras)
    print("\n\n2. MUNICÍPIO COM SEU VALIDADOR ATUAL (ALTERAÇÃO DE REGRAS):")
    print("-"*80)
    buscar_municipio("rio de janeiro", "NOTA CARIOCA")
    
    # Exemplo 3: Município + Validador Existente mas não usado (Migração)
    print("\n\n3. MUNICÍPIO COM VALIDADOR EXISTENTE MAS NÃO USADO (MIGRAÇÃO):")
    print("-"*80)
    buscar_municipio("rio de janeiro", "BETHA")
    
    # Exemplo 4: Município + Validador Novo (Novo Validador)
    print("\n\n4. MUNICÍPIO COM VALIDADOR INEXISTENTE (NOVO VALIDADOR):")
    print("-"*80)
    buscar_municipio("rio de janeiro", "VALIDADOR_TESTE_123")
    
    # Exemplo 5: Município sem validadores cadastrados
    print("\n\n5. MUNICÍPIO SEM VALIDADORES CADASTRADOS:")
    print("-"*80)
    buscar_municipio("acrelandia", "SIAP.NET")
    
    # Exemplo 6: Busca parcial de município
    print("\n\n6. BUSCA PARCIAL DE MUNICÍPIO:")
    print("-"*80)
    buscar_municipio("nova")  # Vai listar sugestões

if __name__ == "__main__":
    main() 