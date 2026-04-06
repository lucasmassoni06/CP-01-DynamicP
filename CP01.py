import pandas as pd

df = pd.read_csv('Check_point_1_dados_logistica_RA_final_par.csv')

#LISTA TUPLA

lista_tupla = []
for _, row in df.iterrows():#Vai passar linha por linha 
    lista_tupla.append(( #Vai adicionar linha por linha do dataframe na lista como tupla
        row['pedido_id'],
        row['produto'],
        row['cidade_destino'],
        row['urgencia'],
        row['tempo_estimado_horas'],
        row['modal']
    ))

for ped in lista_tupla:
    print(ped) # Vai printar tupla por tupla da lista

#DICIONARIO

pedidos_dic = {}
for _, row in df.iterrows(): #Vai passar linha por linha
    pedidos_dic[row['pedido_id']] = { #Cria uma chave para cada id e coloca suas informacoes dentro
            'produto' : row['produto'], 
            'categoria': row['categoria'],
            'cidade_destino': row['cidade_destino'], 
            'quantidade': row['quantidade'], 
            'valor_unitario': row['valor_unitario'], 
            'urgencia': row['urgencia'], 
            'tempo_estimado_horas': row['tempo_estimado_horas'], 
            'modal': row['modal'], 
            'status_pagamento': row['status_pagamento'], 
            'valor_total': row['quantidade'] * row['valor_unitario']
    }

