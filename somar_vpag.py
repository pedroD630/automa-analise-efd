import os
import xml.etree.ElementTree as ET
from decimal import Decimal

def somar_valores_vpag(diretorio):
    soma_total = Decimal('0.00')
    
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.endswith('.xml'):
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)
            try:
                tree = ET.parse(caminho_arquivo)
                root = tree.getroot()

                ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
                
                for vnf in root.findall('.//ns:vNF', ns):
                    valor = Decimal(vnf.text)
                    soma_total += valor

            except Exception as e:
                print(f"Erro ao processar {nome_arquivo}: {e}")
    
    return soma_total

# Exemplo de uso
diretorio = r"C:\Users\Maria Helena\Documents\xml-102"
print(f"Soma total dos valores em <vPag>: R$ {somar_valores_vpag(diretorio):.2f}")
