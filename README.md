# Checkpoint 1 — Dynamic Programming (FIAP)
## Enunciado A — RA com final PAR
### Simulação de Centro de Distribuição com Fila de Pedidos

**Integrantes:**
- Felipe Balbino Murad — RM: 562347
- Lucas Mesquita Massoni — RM: 561686

---

## Como executar

```bash
pip install pandas matplotlib
python checkpoint1_RA_par.py
```

O arquivo `Check_point_1_dados_logistica_RA_final_par.csv` deve estar na mesma pasta.

---

## Estruturas de Dados

| Variável | Estrutura | Uso |
|---|---|---|
| `lista_tupla` | Lista de tuplas | Registro imutável de cada pedido: `(pedido_id, produto, cidade_destino, urgencia, tempo_estimado_horas, modal)` |
| `pedidos_dic` | Dicionário | Acesso O(1) por `pedido_id`; armazena todos os campos incluindo `valor_total = quantidade × valor_unitario` |
| `pedidos_urgencia` | Dicionário de listas | Agrupa IDs por nível de urgência: `alta`, `media`, `baixa` |
| `lista_pedidos` / `lista_ordenada` | Lista | Construída a partir de `pedidos_dic` e ordenada com `sorted()` por urgência e tempo estimado |
| `fila_despacho` | Deque | Fila de saída: urgência alta entra na frente (`appendleft`), demais no final (`append`) |
| `resumo` / `por_modal` | DataFrame | Agrupamentos com `groupby`: valor total por urgência e contagem por modal |

---

## Lógica de Priorização

`sorted()` usa chave composta `lambda`:
1. **Urgência** → `prioridade = {'alta': 1, 'media': 2, 'baixa': 3}`
2. **Tempo estimado** → menor tempo tem precedência dentro do mesmo nível

Pedidos com `status_pagamento != 'ok'` ficam em `aguardando` e não são despachados.

---

## Recursão

| Função | O que faz | Caso base |
|---|---|---|
| `calcular_valor_total(pedidos, indice)` | Soma `valor_total` de todos os pedidos | `indice == len(pedidos)` → retorna `0.0` |
| `contar_pedidos_urgencia(pedidos, nivel, indice)` | Conta pedidos de determinado nível de urgência | `indice == len(pedidos)` → retorna `0` |

---

## Gráficos gerados

- **Gráfico 1** — Valor total por urgência (`resumo` do groupby)
- **Gráfico 2** — Quantidade de pedidos por modal (`por_modal` do groupby)
- **Gráfico 3** — Tempo estimado por produto na ordem de saída do `fila_despacho`

---

## Complexidade (Big O)

| Operação | Big O |
|---|---|
| Acesso a `pedidos_dic` por chave | O(1) |
| `sorted()` — Timsort | O(n log n) |
| `deque` appendleft / popleft | O(1) |
| `calcular_valor_total` | O(n) |
| `contar_pedidos_urgencia` | O(n) |
| `groupby` DataFrame | O(n) |
