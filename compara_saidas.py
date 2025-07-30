def totalizar_saidas(arquivo):
    totais = {}

    with open(arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            campos = linha.strip().split('|')
            if len(campos) < 13:
                continue

            if campos[1] == 'C100':
                ind_oper = campos[2]
                cod_sit = campos[3]
                modelo = campos[5]

                if ind_oper == '1' and cod_sit == '0':
                    try:
                        vl_doc = float(campos[12].replace(',', '.'))
                        if modelo not in totais:
                            totais[modelo] = 0.0
                        totais[modelo] += vl_doc
                    except (ValueError, IndexError):
                        print(f"⚠️ Erro ao processar linha: {campos}")

    return totais


def comparar_saidas(arquivo1, arquivo2):
    totais1 = totalizar_saidas(arquivo1)
    totais2 = totalizar_saidas(arquivo2)

    modelos = sorted(set(totais1.keys()) | set(totais2.keys()))

    print(f"\n🔍 Comparação de Saídas\n{'-'*40}")
    print(f"{'Modelo':<10} {'Arquivo 1':>15} {'Arquivo 2':>15} {'Diferença':>15}")
    print('-' * 60)

    for modelo in modelos:
        total1 = totais1.get(modelo, 0.0)
        total2 = totais2.get(modelo, 0.0)
        diff = total2 - total1

        descricao = {
            '65': 'NFC-e',
            '55': 'NF-e'
        }.get(modelo, f'Mod {modelo}')

        print(f"{descricao:<10} {total1:>15.2f} {total2:>15.2f} {diff:>15.2f}")


# ✅ Exemplo de uso:
comparar_saidas('março-efd-valida.txt', 'Março-Novo.txt')