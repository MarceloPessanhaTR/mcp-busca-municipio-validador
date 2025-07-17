from associar_municipios_validadores import AssociadorMunicipiosValidadores
from datetime import datetime
import unicodedata

def remover_acentos(texto):
    """Remove acentos de uma string"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def buscar_municipio(nome_municipio: str, nome_validador: str = None):
    """
    Busca validadores de um município específico e classifica um novo validador
    
    Args:
        nome_municipio: Nome do município a buscar
        nome_validador: Nome do validador a classificar (opcional)
    """
    
    # Arquivos de entrada
    arquivo_municipios = "PresetFiles/TACES06.TXT"
    arquivo_validadores = "PresetFiles/TFIX105.txt"
    
    # Cria instância do associador
    print(f"=== BUSCANDO VALIDADORES DO MUNICÍPIO: {nome_municipio.upper()} ===")
    if nome_validador:
        print(f"=== ANALISANDO VALIDADOR: {nome_validador.upper()} ===")
    print()
    
    associador = AssociadorMunicipiosValidadores(arquivo_municipios, arquivo_validadores)
    
    # Carrega os dados
    print("Carregando dados...")
    associador.carregar_municipios()
    associador.carregar_validadores()
    
    # Associa os dados
    print("\nAssociando dados...")
    associador.associar_dados()
    
    # Busca o município - melhora a busca para ser mais flexível
    municipios_encontrados = []
    municipios_parciais = []  # Para guardar correspondências parciais
    nome_busca = remover_acentos(nome_municipio.upper().strip())
    
    # Primeira passada: busca exata
    for registro in associador.resultados:
        nome_registro = remover_acentos(registro['descricao'].upper().strip())
        
        # Busca exata primeiro
        if nome_busca == nome_registro:
            municipios_encontrados.append(registro)
        # Guarda correspondências parciais para usar só se não houver exata
        elif nome_busca in nome_registro:
            municipios_parciais.append(registro)
    
    # Se não encontrou correspondência exata, usa as parciais
    if not municipios_encontrados and municipios_parciais:
        print(f"\n⚠️  Não foi encontrado município com nome exato '{nome_municipio}'.")
        print("Encontrados municípios com nomes similares. Mostrando resultados parciais:")
        municipios_encontrados = municipios_parciais
    
    if not municipios_encontrados:
        print(f"\nMunicípio '{nome_municipio}' não encontrado!")
        
        # Sugere municípios similares - busca mais ampla
        print("\nMunicípios com nomes similares:")
        similares = []
        palavras_busca = nome_busca.split()
        
        for registro in associador.resultados:
            nome_registro = remover_acentos(registro['descricao'].upper())
            # Verifica se alguma palavra da busca está no nome
            for palavra in palavras_busca:
                if len(palavra) >= 3 and palavra in nome_registro:
                    if registro not in similares:
                        similares.append(registro)
                        break
        
        # Remove duplicatas e mostra únicos
        municipios_unicos = {}
        for s in similares:
            chave = f"{s['descricao']} ({s['cod_estado']})"
            municipios_unicos[chave] = s
        
        for nome in sorted(municipios_unicos.keys())[:20]:
            print(f"  - {nome}")
            
        return
    
    # Remove duplicatas mantendo apenas registros únicos
    municipios_unicos = {}
    for m in municipios_encontrados:
        chave = (m['cod_estado'], m['cod_municipio'], m['cod_validador'])
        municipios_unicos[chave] = m
    
    municipios_encontrados = list(municipios_unicos.values())
    
    # Separa por município (pode haver mais de um com mesmo nome em estados diferentes)
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
        if registro['cod_validador']:  # Só adiciona se tiver validador
            municipios_por_codigo[chave]['validadores'].append(registro)
    
    # Processa cada município encontrado
    for chave, dados in municipios_por_codigo.items():
        info = dados['info']
        validadores = dados['validadores']
        
        print(f"\n{'='*150}")
        print(f"MUNICÍPIO: {info['nome']} - {info['estado']} (Código: {info['codigo']})")
        print(f"{'='*150}")
        
        if not validadores:
            print("\n❌ Este município NÃO possui validadores cadastrados.")
            if nome_validador:
                print(f"\n📋 CLASSIFICAÇÃO DO VALIDADOR '{nome_validador}':")
                
                # Verifica se o validador existe na lista geral
                validador_existe_geral = False
                
                # Percorre todos os validadores carregados para verificar se existe
                for municipio_validadores in associador.validadores.values():
                    for v in municipio_validadores:
                        if nome_validador.upper() in v['cod_validador'].upper() or \
                           nome_validador.upper() in v['desc_validador'].upper():
                            validador_existe_geral = True
                            break
                    if validador_existe_geral:
                        break
                
                if not validador_existe_geral:
                    print(f"   ✅ NOVO VALIDADOR")
                    print(f"   → Este validador não existe no sistema")
                else:
                    print(f"   ↔️  MIGRAÇÃO DE VALIDADOR")
                    print(f"   → O validador existe no sistema mas nunca foi usado por {info['nome']}")
        else:
            print(f"\n📋 VALIDADORES ATUAIS DO MUNICÍPIO:")
            print(f"{'─'*120}")
            print(f"{'VALIDADOR':^25} | {'DESCRIÇÃO':^35} | {'DT INICIAL':^10} | {'DT VALID':^10} | {'STATUS':^6}")
            print(f"{'─'*120}")
            
            # Ordena validadores por data para identificar o mais atual
            for v in validadores:
                # Pega a data inicial diretamente do registro
                data_inicial = v.get('data_inicial', '')
                
                # Se não tem data de validade, considera como atual
                if not v['valid_validador']:
                    situacao = "ATIVO"
                else:
                    # Verifica se a data de validade já passou
                    try:
                        dia, mes, ano = v['valid_validador'].split('/')
                        data_valid = datetime(int(ano), int(mes), int(dia))
                        if data_valid < datetime.now():
                            situacao = "EXPIRADO"
                        else:
                            situacao = "ATIVO"
                    except:
                        situacao = "ATIVO"
                
                # Formatação mais compacta
                cod_val = v['cod_validador'][:25]
                desc_val = v['desc_validador'][:35]
                status = f"{v['valid_final']}-{situacao}"
                
                print(f"{cod_val:25} | {desc_val:35} | {data_inicial:^10} | {v['valid_validador']:^10} | {status}")
            
            # Identifica o validador mais atual
            validador_atual = None
            for v in validadores:
                if v['valid_final'] == 'S':
                    if not v['valid_validador']:  # Sem data de validade = atual
                        validador_atual = v
                        break
                    else:
                        # Verifica se ainda está válido
                        try:
                            dia, mes, ano = v['valid_validador'].split('/')
                            data_valid = datetime(int(ano), int(mes), int(dia))
                            if data_valid >= datetime.now():
                                if not validador_atual or (validador_atual['valid_validador'] and 
                                    datetime.strptime(validador_atual['valid_validador'], '%d/%m/%Y') < data_valid):
                                    validador_atual = v
                        except:
                            pass
            
            # Se não encontrou nenhum ativo, pega o último da lista
            if not validador_atual and validadores:
                validador_atual = validadores[-1]
            
            print(f"\n🔍 VALIDADOR MAIS ATUAL: {validador_atual['desc_validador'] if validador_atual else 'Nenhum ativo'}")
            
            # Classifica o validador informado
            if nome_validador:
                print(f"\n📋 CLASSIFICAÇÃO DO VALIDADOR '{nome_validador}':")
                
                # Primeiro, verifica se o validador existe na lista geral de validadores
                validador_existe_geral = False
                
                # Percorre todos os validadores carregados para verificar se existe
                for municipio_validadores in associador.validadores.values():
                    for v in municipio_validadores:
                        if nome_validador.upper() in v['cod_validador'].upper() or \
                           nome_validador.upper() in v['desc_validador'].upper():
                            validador_existe_geral = True
                            break
                    if validador_existe_geral:
                        break
                
                # Se não existe na lista geral de validadores
                if not validador_existe_geral:
                    print(f"   ✅ NOVO VALIDADOR")
                    print(f"   → Este validador não existe no sistema")
                else:
                    # O validador existe no sistema, agora verifica se existe para este município
                    validador_existe_municipio = False
                    validador_igual_atual = False
                    
                    for v in validadores:
                        if nome_validador.upper() in v['cod_validador'].upper() or \
                           nome_validador.upper() in v['desc_validador'].upper():
                            validador_existe_municipio = True
                            # Verifica se é o validador atual
                            if validador_atual and (
                                v['cod_validador'] == validador_atual['cod_validador'] or
                                v['desc_validador'] == validador_atual['desc_validador']):
                                validador_igual_atual = True
                            break
                    
                    if not validador_existe_municipio:
                        print(f"   ↔️  MIGRAÇÃO DE VALIDADOR")
                        print(f"   → O validador existe no sistema mas nunca foi usado por {info['nome']}")
                    elif not validador_igual_atual:
                        print(f"   ↔️  MIGRAÇÃO DE VALIDADOR")
                        print(f"   → {info['nome']} já usou este validador, mas não é o atual")
                        print(f"   → Mudança de '{validador_atual['desc_validador'] if validador_atual else 'N/A'}' para '{nome_validador}'")
                    else:
                        print(f"   🔄 ALTERAÇÃO DE REGRAS")
                        print(f"   → {info['nome']} já usa este validador atualmente")

def main():
    """Função principal"""
    import sys
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        
        # Lista de validadores conhecidos (nomes completos)
        validadores_conhecidos = [
            'NFSE ABACO', 'ISS DIGITAL', 'ISS WEB', 'ISS ONLINE', 'ISS.NET',
            'BETHA', 'SIGISS', 'DMS', 'DEISS', 'SIAP.NET', 'NOTA CARIOCA',
            'GOV DIGITAL', 'WEB XML', 'FGMAISS', 'SIMPLISS', 'ATENDENET', 
            'FINTELISS', 'WEBISS', 'MEUISS', 'SUPERNOVA', 'SIGCORP', 'SPE',
            'ISS DIGITAL BH', 'ISS DIGITAL CF', 'NOTA JOSEENSE', 'DES XML',
            'ISS WEB LAR PAULI', 'ISS WEB XML', 'NFSE GIAP', 'ISS ONLINE 4R',
            'DMSTE CAXIAS', 'SPEED GOV', 'SAATRI NFSE', 'REMESSAXML', 
            'DIEF', 'DIEF-SP', 'DIEF-RJ', 'DIFJ', 'DIFSP', 'DIFUB', 'DES', 
            'DEST', 'DESE', 'DESIF', 'DESONLINE', 'DMSE', 'E-GOVERNO', 'EGOVERNO',
            'EISS', 'EFE', 'ERECEITA', 'GEISWEB', 'GIMONLINE', 'GOVDIGITAL',
            'CEISS', 'DECLARARDIR', 'DESGASPAR', 'DESXML', 'DIFJF'
        ]
        
        # Converte argumentos em string única
        args_string = ' '.join(args).upper()
        
        nome_validador = None
        nome_municipio = None
        
        # Primeiro, tenta encontrar um validador conhecido na string
        for validador in sorted(validadores_conhecidos, key=len, reverse=True):
            if validador.upper() in args_string:
                # Encontrou o validador
                pos = args_string.find(validador.upper())
                nome_municipio = args_string[:pos].strip()
                nome_validador = args_string[pos:].strip()
                break
        
        # Se não encontrou validador conhecido, tenta uma abordagem mais genérica
        if nome_validador is None:
            # Procura por palavras-chave comuns em validadores
            validador_keywords = ['ABACO', 'BETHA', 'ISS', 'SIGISS', 'DMS', 'DEISS', 'SIAP', 
                                 'NFSE', 'GOV', 'DIGITAL', 'WEB', 'XML', 'ONLINE', 'NET',
                                 'FGMAISS', 'SIMPLISS', 'ATENDENET', 'FINTELISS', 'NOTA',
                                 'SPE', 'WEBISS', 'MEUISS', 'SUPERNOVA', 'SIGCORP', 'DIEF',
                                 'DIFJ', 'DIFSP', 'DIFUB', 'DES', 'DEST', 'DESE', 'DESIF',
                                 'DESONLINE', 'DMSE', 'EGOVERNO', 'EISS', 'EFE', 'ERECEITA',
                                 'GEISWEB', 'GIMONLINE', 'GOVDIGITAL', 'CEISS', 'DECLARARDIR',
                                 'DESGASPAR', 'DESXML', 'DIFJF']
            
            # Verifica cada palavra
            palavras = args_string.split()
            
            # Estratégia melhorada: procura pela última palavra que pode ser um validador
            # Isso porque o município geralmente vem primeiro
            for i in range(len(palavras) - 1, -1, -1):
                palavra = palavras[i]
                
                # Verifica se é uma palavra-chave de validador
                if any(keyword == palavra for keyword in validador_keywords):
                    # Verifica se faz parte de um nome composto olhando para trás
                    if i > 0:
                        palavra_anterior = palavras[i - 1]
                        # Lista de palavras que podem preceder e formar nomes compostos
                        palavras_precedentes = ['ISS', 'NOTA', 'WEB', 'NFSE', 'GOV', 'SPEED', 'SAATRI']
                        if palavra_anterior in palavras_precedentes:
                            # É parte de um nome composto, continua procurando
                            continue
                    
                    # Encontrou onde começa o validador
                    nome_municipio = ' '.join(palavras[:i])
                    nome_validador = ' '.join(palavras[i:])
                    break
                
                # Se não encontrou por palavra-chave exata, verifica se é uma palavra
                # que parece ser um validador (siglas em maiúsculas com 3+ letras)
                if len(palavra) >= 3 and palavra.isalpha() and i > 0:
                    # Lista de palavras que NÃO devem ser consideradas validadores
                    palavras_nao_validador = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO',
                                            'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO',
                                            'HORIZONTE', 'ALEGRE', 'VISTA', 'CAMPO', 'CAMPOS', 'PRETO',
                                            'VERDE', 'BRANCO', 'CLARO', 'FUNDO', 'GERAIS', 'PAULISTA',
                                            'PAULO', 'CATARINA', 'GROSSO', 'VELHO', 'NOVO', 'NOVA']
                    
                    # Se a palavra está na lista de não-validadores, continua procurando
                    if palavra in palavras_nao_validador:
                        continue
                    
                    # Verifica se as palavras anteriores parecem formar um nome de município
                    palavras_municipio = palavras[:i]
                    if palavras_municipio:
                        # Heurística: se tem palavras comuns de município, separa aqui
                        palavras_comuns_municipio = ['DE', 'DO', 'DA', 'DOS', 'DAS', 'SAO', 'SANTO', 
                                                    'SANTA', 'NOVA', 'NOVO', 'PORTO', 'RIO', 'GRANDE',
                                                    'ALTO', 'BAIXO', 'NORTE', 'SUL', 'LESTE', 'OESTE']
                        if any(p in palavras_comuns_municipio for p in palavras_municipio):
                            nome_municipio = ' '.join(palavras[:i])
                            nome_validador = ' '.join(palavras[i:])
                            break
        
        # Se ainda não separou, assume que todos os argumentos são o município
        if nome_municipio is None:
            nome_municipio = ' '.join(args)
            
        # Remove espaços extras
        nome_municipio = nome_municipio.strip() if nome_municipio else ''
        nome_validador = nome_validador.strip() if nome_validador else None
        
        if nome_municipio:
            buscar_municipio(nome_municipio, nome_validador)
        else:
            print("Uso: python buscar_municipio_validador.py <nome_municipio> [nome_validador]")
            print("Exemplos:")
            print('  python buscar_municipio_validador.py "nova iguacu" "ISS DIGITAL"')
            print('  python buscar_municipio_validador.py sao paulo iss digital')
            print('  python buscar_municipio_validador.py jacarei betha')
    else:
        # Exemplos de uso
        print("\n" + "="*80)
        print("EXEMPLO 1: São Paulo com ISS DIGITAL")
        print("="*80)
        buscar_municipio("sao paulo", "ISS DIGITAL")
        
        print("\n\n" + "="*80)
        print("EXEMPLO 2: Rio de Janeiro")
        print("="*80)
        buscar_municipio("rio de janeiro", "NOTA CARIOCA")

if __name__ == "__main__":
    main() 