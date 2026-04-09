import pandas as pd
from collections import deque
import matplotlib.pyplot as plt

df = pd.read_csv('Check_point_1_dados_logistica_RA_final_par.csv')

print("=========== Checkpoint 1 - Dynamic Programming ===========")
print("====================== Integrantes =======================")
print("============ Felipe Balbino Murad RM: 562347 =============")
print("============ Lucas Mesquita Massoni RM: 561686 ===========")

#Lista tupla

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

#Dicionario + urgencia

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


#Lista + ordenação

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

for i, p in enumerate(lista_ordenada, 1):
    print(f"Pedido #{p['pedido_id']} - {p['produto']} -> {p['cidade_destino']} "
    f"- {p['urgencia'].upper()} - {p['tempo_estimado_horas']}h - R$ {p['valor_total']:.2f}")

# --- Deque — Fila de Despacho ---
# Alta urgência entra na frente (appendleft); demais entram no final (append)
fila_despacho = deque()

for pedido in lista_ordenada:
    if pedido['urgencia'] == 'alta':
        fila_despacho.appendleft(pedido)
    else:
        fila_despacho.append(pedido)

print('=' * 55)
print('\n=== Fila de Despacho ===\n')
for i, p in enumerate(fila_despacho, 1):
    print(f"Pedido #{p['pedido_id']} - {p['produto']} -> {p['cidade_destino']} "
    f"- {p['urgencia'].upper()} - {p['tempo_estimado_horas']}h - {p['modal']}")

# Processa a fila: despacha pedidos com pagamento ok, retém os pendentes
print('=' * 55)
print('\n=== Simulação de Despacho ===\n')
despachados = []
aguardando  = []

temp_fila = deque(fila_despacho)
while temp_fila:
    pedido = temp_fila.popleft()
    if pedido['status_pagamento'] == 'ok':
        despachados.append(pedido)
        print(f"  DESPACHADO -> Pedido #{pedido['pedido_id']} - {pedido['produto']} -> {pedido['cidade_destino']}")
    else:
        aguardando.append(pedido)
        print(f"  AGUARDANDO -> Pedido #{pedido['pedido_id']} - {pedido['produto']} (pagamento pendente)")

print(f'\nTotal despachados: {len(despachados)} | Aguardando: {len(aguardando)}')

# Recursão
# Soma o valor_total de todos os pedidos da lista recursivamente
def calcular_valor_total(pedidos, indice=0):
    if indice == len(pedidos):   # caso base: fim da lista
        return 0.0
    return pedidos[indice]['valor_total'] + calcular_valor_total(pedidos, indice + 1)

# Conta pedidos com determinado nível de urgência recursivamente
def contar_pedidos_urgencia(pedidos, nivel, indice=0):
    if indice == len(pedidos):   # caso base: fim da lista
        return 0
    match = 1 if pedidos[indice]['urgencia'] == nivel else 0
    return match + contar_pedidos_urgencia(pedidos, nivel, indice + 1)

valor_total_geral = calcular_valor_total(lista_ordenada)
qtd_alta  = contar_pedidos_urgencia(lista_ordenada, 'alta')
qtd_media = contar_pedidos_urgencia(lista_ordenada, 'media')
qtd_baixa = contar_pedidos_urgencia(lista_ordenada, 'baixa')

print()
print('=== Resultados da Recursão ===')
print(f'  Renda bruta: R$ {valor_total_geral:.2f}')
print(f'  ALTA:  {qtd_alta} pedido(s)')
print(f'  MÉDIA: {qtd_media} pedido(s)')
print(f'  BAIXA: {qtd_baixa} pedido(s)')

# Dataframe — análise agregada
df['valor_total'] = df['quantidade'] * df['valor_unitario']

# Soma do valor total agrupado por nivel de urgencia
resumo = df.groupby('urgencia')['valor_total'].sum()

print()
print('=== Valor Total por Urgência (DataFrame) ===')
print(resumo.to_string())

# Contagem de pedidos agrupados por modal de transporte
por_modal = df.groupby('modal')['pedido_id'].count()
print()
print('=== Pedidos por Modal ===')
print(por_modal.to_string())

# --- GRÁFICOS ---
# Gráfico 1: valor total por urgência
plt.title('Valor Total por Urgência')
plt.xlabel('Urgência')
plt.ylabel('Valor Total (R$)')
plt.plot(resumo.index.tolist(), resumo.values.tolist(), marker='o', color='steelblue')
plt.grid(True)
plt.show()

# Gráfico 2: quantidade de pedidos por modal
plt.title('Pedidos por Modal')
plt.xlabel('Modal')
plt.ylabel('Quantidade')
plt.plot(por_modal.index.tolist(), por_modal.values.tolist(), marker='o', color='#e74c3c')
plt.grid(True)
plt.show()

# Gráfico 3: tempo estimado na ordem de despacho do deque
produtos_ordem = [p['produto'] for p in fila_despacho]
tempos_ordem   = [p['tempo_estimado_horas'] for p in fila_despacho]

plt.title('Tempo Estimado por Ordem de Despacho')
plt.xlabel('Produto')
plt.ylabel('Tempo Estimado (horas)')
plt.plot(produtos_ordem, tempos_ordem, marker='o', color='#2ecc71')
plt.grid(True)
plt.show()

print()
print('=' * 55)
print('     RELATÓRIO FINAL — CENTRO DE DISTRIBUIÇÃO')
print('=' * 55)
print(f'  Total de pedidos:          {len(df)}')
print(f'  Urgência ALTA:             {qtd_alta}')
print(f'  Urgência MÉDIA:            {qtd_media}')
print(f'  Urgência BAIXA:            {qtd_baixa}')
print(f'  Valor total da carteira:   R$ {valor_total_geral:.2f}')
print(f'  Despachados:               {len(despachados)}')
print(f'  Aguardando pagamento:      {len(aguardando)}')
print()
print('  --- Big O ---')
print('  Dicionário (acesso):       O(1)')
print('  sorted() — Timsort:        O(n log n)')
print('  deque appendleft/popleft:  O(1)')
print('  Recursão valor/contagem:   O(n)')
print('  groupby DataFrame:         O(n)')
print('=' * 55)
