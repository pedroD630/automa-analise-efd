# automa-analise-efd
Scripts para automatizar análise de arquivos efd e encontrar diferenças e alterações nos arquivos, a fim de corrigir internamente no sistema erp Arius

⚙️ Funcionalidades

    Totalização de entradas (modelo 55) por data

    Totalização de saídas (modelo 65 e 55) por data

    Separação entre NFe e NFCe

    Comparação entre dois arquivos de EFD (entradas ou saídas)

  Os scripts esperam arquivos no formato .txt, gerados pelo validador do SPED Fiscal (como o EFD-VALIDA).

  Exemplo de linha analisada. Os campos analisados podem ser alterados dependendo do objetivo. 

  |C100|1|0||65|00|105|16868|31250302434299000118651050000168681000285093|01032025|01032025|103,6|0|0|0|103,6|9|0|0|0|7,9|1,42||||||||

    Campo 1: C100 → Registro de nota fiscal

    Campo 2: 1 → Indicador de operação (1 = saída)

    Campo 9: Chave documento

    Campo 12: Valor do documento (vl_doc)

Exemplos de uso:

##compara.py

Abre e lÊ um arquivo txt. Gera um array de objetos (nota_atual) onde inclui todos os registros C100 e C130 que são lidos.
A linha if campos[2] == '0', indica que serão filtrados apenas notas de entrada. No padrão da efd, o segundo campo sendo = 1 indica saída e 0 indica entrada
Realiza a leitura de dois arquivos, onde deve ser indicado o atual e o anterior e insere num arquivo o resultado da analise. Também mostra lado a lado os seguintes dados das notas:
                        'fornecedor',
                        'modelo',
                        'numero',
                        'data_emissao',
                        'data_entrada',
                        'valor_total'

O nome do arquivo de saida deve ser indicado: 
Exemplo:

 with open('comparativo_notas-março.txt', 'w', encoding='utf-8') as f:
