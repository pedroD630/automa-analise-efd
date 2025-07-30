def totalizar_saidas_por_modelo(arquivo):
    totais = {}

    with open(arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            campos = linha.strip().split('|')

            if len(campos) < 13:
                continue  # ignora linhas incompletas

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

    print("🔢 Totais de Saída por Modelo:")
    for modelo, total in totais.items():
        descricao = {
            '65': 'NFC-e',
            '55': 'NF-e'
        }.get(modelo, f'Modelo {modelo}')
        print(f"- {descricao}: R$ {total:.2f}")

    return totais


# Exemplo de uso:
arquivo = 'março-efd-valida.txt'
totalizar_saidas_por_modelo(arquivo)