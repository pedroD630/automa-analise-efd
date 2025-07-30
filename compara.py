import pandas as pd

def parse_efd(filepath):
    with open(filepath, 'r', encoding='latin1') as f:
        linhas = f.readlines()

    notas = []
    modelos_aceitos = {'01', '1B', '04', '06', '21', '22', '55', '29', '66', '07'}

    nota_atual = None

    for linha in linhas:
        campos = linha.strip().split('|')

        if len(campos) < 2:
            continue

        registro = campos[1]
        ##ind_oper = campos[2]

        if registro == 'C100' and len(campos) >= 13:
            modelo = campos[5].strip().upper().lstrip('0')

            if campos[2] == '0' and modelo in modelos_aceitos:
                try:
                    nota_atual = {
                        'fornecedor': campos[4],
                        'modelo': modelo,
                        'numero': campos[8],
                        'data_emissao': campos[10],
                        'data_entrada': campos[11],
                        'valor_total': float(campos[12].replace(',', '.')),
                        'c113': []
                    }
                    notas.append(nota_atual)
                except (ValueError, IndexError):
                    continue
        

        elif registro == 'C113' and nota_atual:
            nota_atual['c113'].append('|'.join(campos))

    return pd.DataFrame(notas)

def comparar_efd(arquivo_antigo, arquivo_novo):
    df_antigo = parse_efd(arquivo_antigo)
    df_novo = parse_efd(arquivo_novo)

    df_antigo['c113'] = df_antigo['c113'].astype(str)
    df_novo['c113'] = df_novo['c113'].astype(str)

    # Mescla pelos números das notas
    comparativo = pd.merge(
        df_antigo,
        df_novo,
        on='numero',
        how='outer',
        suffixes=('_antigo', '_novo'),
        indicator=True
    )

    import ast

    comparativo['c113_antigo'] = comparativo['c113_antigo'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    comparativo['c113_novo'] = comparativo['c113_novo'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    comparativo['diferença'] = comparativo['valor_total_novo'] - comparativo['valor_total_antigo']

    print("\n📌 COMPARATIVO NOTA A NOTA:")
    print(comparativo[['numero', 'valor_total_antigo', 'valor_total_novo', 'diferença', '_merge']])

    print("\nNotas só no NOVO:")
    print(comparativo[comparativo['_merge'] == 'right_only'][['numero', 'valor_total_novo']])

    print("\nNotas só no ANTIGO:")
    print(comparativo[comparativo['_merge'] == 'left_only'][['numero', 'valor_total_antigo']])

    diferentes = comparativo[comparativo['diferença'].abs() > 0.01]

    print("\nNotas com valores diferentes:")
    print(diferentes[['numero', 'valor_total_antigo', 'valor_total_novo', 'diferença']])

    print("\nNotas com valor MAIOR no NOVO:")
    print(diferentes[diferentes['diferença'] > 0][['numero', 'diferença']])

    print("\nTotais gerais:")
    print(f"Soma total no ANTIGO: {df_antigo['valor_total'].sum():,.2f}")
    print(f"Soma total no NOVO:   {df_novo['valor_total'].sum():,.2f}")

    print("\nTotal de notas de entrada:")
    print(f"Arquivo ANTIGO: {len(df_antigo)} notas")
    print(f"Arquivo NOVO:   {len(df_novo)} notas")

    with open('comparativo_notas-março.txt', 'w', encoding='utf-8') as f:
        f.write("COMPARATIVO NOTA A NOTA\n")
        f.write("{:<15} {:>20} {:>20} {:>15} {:>10}\n".format(
            "Número da Nota", "Total no ANTIGO", "Total no NOVO", "Diferença", "Origem"
        ))
        f.write("-" * 85 + "\n")

        for _, row in comparativo.iterrows():
            f.write("{:<15} {:>20,.2f} {:>20,.2f} {:>15,.2f} {:>10}\n".format(
                row['numero'],
                row['valor_total_antigo'] if pd.notnull(row['valor_total_antigo']) else 0,
                row['valor_total_novo'] if pd.notnull(row['valor_total_novo']) else 0,
                row['diferença'] if pd.notnull(row['diferença']) else 0,
                row['_merge']
            ))

            # Adiciona registros C113, se houver
            if '_merge' in row and row['_merge'] in ['both', 'left_only', 'right_only']:
                for origem in ['antigo', 'novo']:
                    campo = f'c113_{origem}'
                    if campo in row and isinstance(row[campo], list):
                        for linha_c113 in row[campo]:
                            f.write(f"   ↳ [{origem}] {linha_c113}\n")

        f.write("\n\nTOTAL DE NOTAS:\n")
        f.write(f"Arquivo ANTIGO: {len(df_antigo)} notas\n")
        f.write(f"Arquivo NOVO:   {len(df_novo)} notas\n")

        f.write("\nTOTAL GERAL DE VALORES:\n")
        f.write(f"Soma ANTIGO: {df_antigo['valor_total'].sum():,.2f}\n")
        f.write(f"Soma NOVO:   {df_novo['valor_total'].sum():,.2f}\n")

# ==== USO ====
arquivo_antigo = 'fevereiro-reginaldo.txt'
arquivo_novo = '02-Novo.txt'

comparar_efd(arquivo_antigo, arquivo_novo)
