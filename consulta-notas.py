import re
import os

def extrair_dados_nfe(arquivo_txt):
    nfe_dados = []
    with open(arquivo_txt, 'r', encoding='latin-1') as arquivo:
        for linha in arquivo:
            if linha.startswith('|C100|'):
                campos = linha.strip().split('|')
                if len(campos) > 9 and campos[5] in ('55', '01'):
                    numero_nfe = campos[8]
                    chave_nfe = campos[9]
                    nfe_dados.append((numero_nfe, chave_nfe))
    return nfe_dados

def gerar_query_oracle(nfe_dados):
    union_selects = "\n        UNION ALL ".join([
        f"SELECT '{numero}' AS NUM_DOC, '{chave}' AS CHV_NFE FROM dual" for numero, chave in nfe_dados
    ])

    query = f"""
    SELECT * FROM (
        {union_selects}
    ) dados
    WHERE NOT EXISTS (
        SELECT 1 FROM fis_t_c100 t
        WHERE (
            t.NUM_DOC = dados.NUM_DOC AND t.CHV_NFE = dados.CHV_NFE
        )
    );
    """
    return query

def dividir_em_blocos(lista, tamanho):
    for i in range(0, len(lista), tamanho):
        yield lista[i:i + tamanho]

# Uso
if __name__ == '__main__':
    arquivo = 'efd-fev.txt'
    dados_nfe = extrair_dados_nfe(arquivo)

    if not dados_nfe:
        print("Nenhum dado encontrado.")
    else:
        blocos = list(dividir_em_blocos(dados_nfe, 999))
        for i, bloco in enumerate(blocos, 1):
            query_sql = gerar_query_oracle(bloco)
            nome_arquivo = f'saida_query_oracle_parte{i}.txt'
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(query_sql)
            print(f"Gerado: {nome_arquivo}")
