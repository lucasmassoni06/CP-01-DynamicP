import pandas as pd

df = pd.read_csv('Check_point_1_dados_logistica_RA_final_par.csv')

print("=========== Checkpoint 1 - Dynamic Programming ===========")
print("====================== Integrantes =======================")
print("============ Felipe Balbino Murad RM: 562347 =============")
print("============ Lucas Mesquita Massoni RM: 561686 ===========")

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


# Vai printar tupla por tupla da lista

print("\nLista Tupla\n")
for ped in lista_tupla:
    print(ped)

#DICIONARIO + URGENCIA

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


#Pega o nivel de urgencia de cada elemento e coloca o id na sua respectiva urgencia
pedidos_urgencia = {"alta" : [], "media" : [], "baixa" : []}
for pid, dados in pedidos_dic.items():
    pedidos_urgencia[dados["urgencia"]].append(pid)


#Printar o dicionario e o de urgencia

print('=' * 55)
print("\nDicionario e pedidos com urgencia\n")

for pid, dados in pedidos_dic.items():
    print(f"{pid} :\n | {dados['produto']} \n | {dados['categoria']} \n | {dados['cidade_destino']}"
                f"\n | {dados['quantidade']} \n | {dados['valor_unitario']} \n | {dados['urgencia']}"
                f"\n | {dados['tempo_estimado_horas']} \n | {dados['modal']} \n | {dados['status_pagamento']}"
                f"\n | {dados['valor_total']}\n")



print("\nURGENICA\n")
for urg, pid in pedidos_urgencia.items():
    print(f"Os seguintes pedidos {pid} tem o nivel de urgencia {urg}.")


#LISTA + ORDENACAO

#Dar valor para cada nivel de urgencia
prioridade = {'alta': 1, 'media': 2, 'baixa': 3}

#Cria a lista de pedidos
lista_pedidos = []
for pid, dados in pedidos_dic.items():
    lista_pedidos.append({
        'pedido_id':            pid,
        'produto':              dados['produto'],
        'cidade_destino':       dados['cidade_destino'],
        'urgencia':             dados['urgencia'],
        'tempo_estimado_horas': dados['tempo_estimado_horas'],
        'modal':                dados['modal'],
        'valor_total':          dados['valor_total'],
        'status_pagamento':     dados['status_pagamento'],
    })

#Ordenar a lista de acordo com urgencia e tempo estimado
lista_ordenada = sorted(lista_pedidos, key=lambda x: (prioridade[x['urgencia']], x['tempo_estimado_horas']))

print('=' * 55)
print("\nLista dos pedidos ordenados por urgencia\n")

for pid, dados in lista_ordenada: