from collections import defaultdict
from datetime import datetime

def ler_saidas_por_data(arquivo):
    totais_por_data = defaultdict(float)

    with open(arquivo, encoding="latin-1") as f:
        for linha in f:
            if "|C100|" in linha:
                campos = linha.strip().split("|")
                try:
                    if len(campos) < 12 or campos[2] != "1":
                        continue
                    
                    data = campos[11]
                    vl_doc = campos[12].replace(",", ".").strip()
                    
                    if not data or not vl_doc:
                        continue
                    
                    # Converter data para formato legível
                    data_formatada = datetime.strptime(data, "%d%m%Y").strftime("%d/%m/%Y")
                    valor = float(vl_doc)
                    totais_por_data[data_formatada] += valor

                except Exception as e:
                    print(f"⚠️ Erro ao processar linha: {campos}\nErro: {e}")
                    continue

    return dict(sorted(totais_por_data.items()))

def comparar_saidas_por_data(arquivo1, arquivo2):
    saidas1 = ler_saidas_por_data(arquivo1)
    saidas2 = ler_saidas_por_data(arquivo2)

    todas_datas = sorted(set(saidas1) | set(saidas2))

    print(f"{'Data':<12} {'Arq1 (R$)':>12} {'Arq2 (R$)':>12} {'Diferença (R$)':>17}")
    print("-" * 55)
    
    for data in todas_datas:
        v1 = saidas1.get(data, 0.0)
        v2 = saidas2.get(data, 0.0)
        diff = v1 - v2
        print(f"{data:<12} {v1:12.2f} {v2:12.2f} {diff:17.2f}")

comparar_saidas_por_data('março-efd-valida.txt', 'Março-Novo.txt')