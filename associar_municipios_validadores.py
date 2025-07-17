import os
from collections import defaultdict
from datetime import datetime

class AssociadorMunicipiosValidadores:
    """Classe para associar dados de municípios com validadores"""
    
    def __init__(self, arquivo_municipios: str, arquivo_validadores: str):
        self.arquivo_municipios = arquivo_municipios
        self.arquivo_validadores = arquivo_validadores
        self.municipios = {}
        self.validadores = defaultdict(list)
        self.resultados = []
        
    def carregar_municipios(self):
        """Carrega dados dos municípios do arquivo TACES06.TXT"""
        try:
            with open(self.arquivo_municipios, 'r', encoding='latin-1') as arquivo:
                linhas = arquivo.readlines()
                
            for linha in linhas:
                if linha.strip():
                    campos = linha.strip().split('\t')
                    if len(campos) >= 8:
                        cod_estado = campos[0].strip()
                        cod_municipio = int(campos[1]) if campos[1].strip() else 0
                        descricao = campos[2].strip()
                        
                        chave = (cod_estado, cod_municipio)
                        self.municipios[chave] = {
                            'cod_estado': cod_estado,
                            'cod_municipio': cod_municipio,
                            'descricao': descricao
                        }
            
            print(f"Total de municípios carregados: {len(self.municipios)}")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar municípios: {e}")
            return False
    
    def formatar_data(self, data_str: str) -> str:
        """Formata uma data do formato YYYYMMDD para DD/MM/YYYY"""
        if not data_str or data_str == '' or len(data_str) < 8:
            return ''
        
        try:
            # Remove espaços e verifica se é uma data válida
            data_str = data_str.strip()
            if data_str == '19000101':  # Data padrão para "sem data"
                return ''
            
            ano = data_str[:4]
            mes = data_str[4:6]
            dia = data_str[6:8]
            
            # Valida se são números
            if ano.isdigit() and mes.isdigit() and dia.isdigit():
                return f"{dia}/{mes}/{ano}"
            else:
                return ''
        except:
            return ''
    
    def carregar_validadores(self):
        """Carrega dados dos validadores do arquivo TFIX105.txt"""
        try:
            with open(self.arquivo_validadores, 'r', encoding='latin-1') as arquivo:
                linhas = arquivo.readlines()
                
            for linha in linhas:
                if linha.strip():
                    campos = linha.strip().split('\t')
                    if len(campos) >= 6:
                        cod_estado = campos[0].strip()
                        cod_municipio = int(campos[1]) if campos[1].strip() else 0
                        cod_validador = campos[2].strip()
                        desc_validador = campos[3].strip()
                        data_inicial = campos[4].strip() if len(campos) > 4 else ''
                        
                        # O campo valid_validador é a data no índice 18 (19º campo)
                        valid_validador = ''
                        if len(campos) > 18:
                            valid_validador = self.formatar_data(campos[18].strip())
                        
                        # O campo valid_final parece ser um status S/N no índice 17 (18º campo)
                        valid_final = 'N'
                        if len(campos) > 17:
                            valid_final = campos[17].strip() if campos[17].strip() in ['S', 'N'] else 'N'
                        
                        chave = (cod_estado, cod_municipio)
                        self.validadores[chave].append({
                            'cod_validador': cod_validador,
                            'desc_validador': desc_validador,
                            'data_inicial': self.formatar_data(data_inicial),
                            'valid_validador': valid_validador,  # Data de validação
                            'valid_final': valid_final  # Status S/N
                        })
            
            print(f"Total de registros de validadores carregados: {sum(len(v) for v in self.validadores.values())}")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar validadores: {e}")
            return False
    
    def associar_dados(self):
        """Associa os dados de municípios com validadores"""
        for chave, municipio in self.municipios.items():
            if chave in self.validadores:
                for validador in self.validadores[chave]:
                    self.resultados.append({
                        'cod_estado': municipio['cod_estado'],
                        'cod_municipio': municipio['cod_municipio'],
                        'descricao': municipio['descricao'],
                        'cod_validador': validador['cod_validador'],
                        'desc_validador': validador['desc_validador'],
                        'data_inicial': validador['data_inicial'],  # Adicionar data_inicial
                        'valid_validador': validador['valid_validador'],
                        'valid_final': validador['valid_final']
                    })
            else:
                # Município sem validador
                self.resultados.append({
                    'cod_estado': municipio['cod_estado'],
                    'cod_municipio': municipio['cod_municipio'],
                    'descricao': municipio['descricao'],
                    'cod_validador': '',
                    'desc_validador': 'SEM VALIDADOR',
                    'data_inicial': '',  # Adicionar data_inicial vazia
                    'valid_validador': '',
                    'valid_final': 'N'
                })
        
        print(f"\nTotal de registros associados: {len(self.resultados)}")
    
    def filtrar_por_estado(self, estado: str):
        """Retorna apenas os registros de um estado específico"""
        return [r for r in self.resultados if r['cod_estado'] == estado]
    
    def exibir_resultados(self, filtro_estado=None, limite=None):
        """Exibe os resultados da associação"""
        dados = self.resultados
        if filtro_estado:
            dados = self.filtrar_por_estado(filtro_estado)
            print(f"\n=== MUNICÍPIOS COM VALIDADORES - {filtro_estado} ===")
        else:
            print("\n=== MUNICÍPIOS COM VALIDADORES ===")
        
        print("-" * 140)
        print(f"{'UF':2} | {'CÓD':4} | {'MUNICÍPIO':40} | {'CÓD VAL':20} | {'VALIDADOR':30} | {'DT VALID':10} | {'FINAL':5}")
        print("-" * 140)
        
        total = len(dados)
        for i, registro in enumerate(dados):
            if limite and i >= limite:
                print(f"\n... e mais {total - limite} registros")
                break
                
            print(f"{registro['cod_estado']:2} | {registro['cod_municipio']:4d} | "
                  f"{registro['descricao'][:40]:40} | {registro['cod_validador'][:20]:20} | "
                  f"{registro['desc_validador'][:30]:30} | {registro['valid_validador']:10} | "
                  f"{registro['valid_final']:5}")
    
    def salvar_resultado(self, arquivo_saida: str, filtro_estado=None):
        """Salva o resultado em arquivo"""
        dados = self.resultados
        if filtro_estado:
            dados = self.filtrar_por_estado(filtro_estado)
            
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("ASSOCIAÇÃO DE MUNICÍPIOS COM VALIDADORES\n")
            f.write("=" * 140 + "\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            if filtro_estado:
                f.write(f"Estado: {filtro_estado}\n")
            f.write("=" * 140 + "\n\n")
            
            f.write(f"{'UF':2} | {'CÓD':4} | {'MUNICÍPIO':40} | {'CÓD VALIDADOR':20} | "
                   f"{'DESC VALIDADOR':30} | {'DT VALID':10} | {'FINAL':5}\n")
            f.write("-" * 140 + "\n")
            
            for registro in dados:
                f.write(f"{registro['cod_estado']:2} | {registro['cod_municipio']:4d} | "
                       f"{registro['descricao'][:40]:40} | {registro['cod_validador'][:20]:20} | "
                       f"{registro['desc_validador'][:30]:30} | {registro['valid_validador']:10} | "
                       f"{registro['valid_final']:5}\n")
            
            f.write("\n" + "=" * 140 + "\n")
            f.write(f"Total de registros: {len(dados)}\n")
            
        print(f"\nResultado salvo em: {arquivo_saida}")

def main():
    """Função principal"""
    # Arquivos de entrada
    arquivo_municipios = "PresetFiles/TACES06.TXT"
    arquivo_validadores = "PresetFiles/TFIX105.txt"
    
    # Cria instância do associador
    associador = AssociadorMunicipiosValidadores(arquivo_municipios, arquivo_validadores)
    
    # Carrega os dados
    print("Carregando dados dos municípios...")
    if not associador.carregar_municipios():
        return
    
    print("\nCarregando dados dos validadores...")
    if not associador.carregar_validadores():
        return
    
    # Associa os dados
    print("\nAssociando dados...")
    associador.associar_dados()
    
    # Exibe alguns resultados
    associador.exibir_resultados(limite=20)
    
    # Exibe resultados do RJ
    associador.exibir_resultados(filtro_estado='RJ', limite=20)
    
    # Salva resultados
    associador.salvar_resultado("municipios_validadores_completo.txt")
    associador.salvar_resultado("municipios_validadores_RJ.txt", filtro_estado='RJ')
    
    # Estatísticas
    print("\n=== ESTATÍSTICAS ===")
    estados_com_validador = set()
    municipios_com_validador = 0
    
    for registro in associador.resultados:
        if registro['cod_validador']:
            estados_com_validador.add(registro['cod_estado'])
            municipios_com_validador += 1
    
    print(f"Total de municípios: {len(associador.municipios)}")
    print(f"Municípios com validador: {municipios_com_validador}")
    print(f"Municípios sem validador: {len(associador.municipios) - municipios_com_validador}")
    print(f"Estados com pelo menos um validador: {len(estados_com_validador)}")

if __name__ == "__main__":
    main() 