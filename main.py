import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Semente aleatória para manter os resultados reproduzíveis
rng = np.random.default_rng(42)

# Quantidade de registros da base
quantidade_registros = 200

# Tipos de locais comerciais onde pode ocorrer a recarga
tipos_local = [
    "shopping",
    "supermercado",
    "estacionamento",
    "centro_empresarial",
    "eletroposto_comercial"
]

# Perfis de usuários do sistema
perfis_usuario = [
    "visitante",
    "funcionario",
    "mensalista",
    "motorista_app",
    "frotista"
]

# Categorias de veículos elétricos e suas faixas aproximadas de bateria em kWh
categorias_veiculo = {
    "compacto_eletrico": (35, 50),
    "sedan_eletrico": (50, 75),
    "suv_eletrico": (70, 100),
    "van_eletrica": (80, 120),
    "utilitario_eletrico": (60, 95)
}

#Lista onde cada sessão de recarga será armazenada
dados = []

#Dicionário para converter número do dia da semana para texto
dias_semana = {
    0: "segunda",
    1: "terca",
    2: "quarta",
    3: "quinta",
    4: "sexta",
    5: "sabado",
    6: "domingo"
}

#--------------------Criando sessões de recarga---------------
for i in range(1, quantidade_registros + 1):
    #Gerando atributo de id da sessão
    id_sessao = f"S{i:03d}" #Atributo que identifica cada sessão como única com 3 digitos.

    #Gerando data da sessão
    data_inicial = datetime(2026, 1, 1) #Definindo limite inicial de data
    dias_aleatorios = rng.integers(0, 90) #Definindo intervalo em dias
    data_sessao = data_inicial + timedelta(days=int(dias_aleatorios)) #Somando data inicial + intervalo de dias para se obter a data do registro

    #Identificação do dia da semana
    dia_semana = dias_semana[data_sessao.weekday()]

    #Geração da hora de inicio da sessão
    hora_inicio = rng.integers(0, 24)

    #Classificação da hora em período do dia
    if 6 <= hora_inicio <= 11:
        periodo_dia = "manha"
    elif 12 <= hora_inicio <= 17:
        periodo_dia = "tarde"
    elif 18 <= hora_inicio <= 23:
        periodo_dia = "noite"
    else:
        periodo_dia = "madrugada"

    #Esclha aleatória das prinicipais categorias da sessão
    tipo_local = rng.choice(tipos_local)
    perfil_usuario = rng.choice(perfis_usuario)
    categoria_veiculo = rng.choice(list(categorias_veiculo.keys()))

    # Busca da faixa da bateria correspondete ao veículo escolhido
    capacidade_minima, capacidade_maxima = categorias_veiculo[categoria_veiculo]

    #Geração da capacidade da bateria dentro da faixa adequada
    capacidade_bateria_kwh = round( #Função que arredonda casas decimais
        rng.uniform(capacidade_minima, capacidade_maxima), 2
    )

    # Percentual da bateria no inicio da recarga
    bateria_inicial_pct = round(
        rng.uniform(10,60), 2
    )

    #Percentual que será adicionado durante a recarga
    aumento_bateria_pct = rng.uniform(20, 60)

    # Cálculo da bateria final
    bateria_final_pct = bateria_inicial_pct + aumento_bateria_pct

    # Limite máximo
    if bateria_final_pct > 100:
        bateria_final_pct = 100

    bateria_final_pct = round(bateria_final_pct, 2)

    #Diferença entre bateria final e inicial
    variacao_bateria_pct = round(
        bateria_final_pct - bateria_inicial_pct, 2
    )

    #Energia consumida na sessão
    energia_consumida_kwh = round(
        capacidade_bateria_kwh * (variacao_bateria_pct/100), 2
    )

    #Potência média do carregador, em situações reais fica entre 22kw a 45kw
    potencia_media_kw = round(
        rng.uniform(22, 45),
        2
    )

    #Duração da recarga em minutos
    duracao_recarga_min = round(
        (energia_consumida_kwh / potencia_media_kw) * 60
    )

    #Ocupação do local(varia conforme o período do dia)
    match periodo_dia:
        case "manha":
            ocupacao_local_pct = rng.uniform(25, 65)
        case "tarde":
            ocupacao_local_pct = rng.uniform(45, 85)
        case "noite":
            ocupacao_local_pct = rng.uniform(50,  95)
        case "madrugada":
            ocupacao_local_pct = rng.uniform(5, 30)

    #Ajuste com base no local
    if tipo_local == "shopping":
        ocupacao_local_pct += 8
    elif tipo_local == "centro_empresarial" and periodo_dia in ["manha", "tarde"]:
        ocupacao_local_pct += 10
    elif tipo_local == "eletroposto_comercial":
        ocupacao_local_pct -= 5

    # Garante que a ocupação fique entre 0% e 100%
    if ocupacao_local_pct < 0:
        ocupacao_local_pct = 0
    elif ocupacao_local_pct > 100:
        ocupacao_local_pct = 100

    ocupacao_local_pct = round(ocupacao_local_pct, 2)

    # A fila é influenciada pela ocupação do local.
    if ocupacao_local_pct < 50:
        fila_espera_min = rng.integers(0, 6)
    elif ocupacao_local_pct < 75:
        fila_espera_min = rng.integers(5, 16)
    else:
        fila_espera_min = rng.integers(15, 36)

    # Tarifas médias por tipo de local
    tarifas_por_local = {
        "shopping": 2.40,
        "supermercado": 2.15,
        "estacionamento": 2.25,
        "centro_empresarial": 2.35,
        "eletroposto_comercial": 2.70
    }

    tarifa_kwh = tarifas_por_local[tipo_local]

    # Ajuste de tarifa conforme o período do dia
    if periodo_dia == "tarde":
        tarifa_kwh += 0.10
    elif periodo_dia == "noite":
        tarifa_kwh += 0.15
    elif periodo_dia == "madrugada":
        tarifa_kwh -= 0.20

    tarifa_kwh = round(tarifa_kwh, 2)

    # Custo da energia consumida
    custo_energia = round(
        energia_consumida_kwh * tarifa_kwh,
        2
    )

    # Taxa de serviço por tipo de local
    taxas_por_local = {
        "shopping": 6.00,
        "supermercado": 4.00,
        "estacionamento": 5.00,
        "centro_empresarial": 5.50,
        "eletroposto_comercial": 7.00
    }

    taxa_servico = taxas_por_local[tipo_local]

    # Custo total da sessão
    custo_total = round(
        custo_energia + taxa_servico,
        2
    )

    #----------------Armazenamento dos dados--------------------
    dados.append({
        "id_sessao": id_sessao,
        "data_sessao": data_sessao.date(),
        "dia_semana": dia_semana,
        "hora_inicio": hora_inicio,
        "periodo_dia": periodo_dia,
        "tipo_local": tipo_local,
        "perfil_usuario": perfil_usuario,
        "categoria_veiculo": categoria_veiculo,
        "capacidade_bateria_kwh": capacidade_bateria_kwh,
        "bateria_inicial_pct": bateria_inicial_pct,
        "bateria_final_pct": bateria_final_pct,
        "variacao_bateria_pct": variacao_bateria_pct,
        "energia_consumida_kwh": energia_consumida_kwh,
        "potencia_media_kw": potencia_media_kw,
        "duracao_recarga_min": duracao_recarga_min,
        "ocupacao_local_pct": ocupacao_local_pct,
        "fila_espera_min": fila_espera_min,
        "tarifa_kwh": tarifa_kwh,
        "custo_energia": custo_energia,
        "taxa_servico": taxa_servico,
        "custo_total": custo_total
    })

#Transformação da lista de dados em uma tabela
df = pd.DataFrame(dados)
# -------------------- Validação da base --------------------
print("\n-------------------- VALIDAÇÃO DA BASE --------------------")

# 1. Validação da quantidade mínima de linhas
validacao_linhas = df.shape[0] >= 100

# 2. Validação da quantidade mínima de colunas
validacao_colunas = df.shape[1] >= 15

# 3. Validação de IDs únicos
validacao_ids_unicos = df["id_sessao"].is_unique

# 4. Validação de ausência de valores nulos
validacao_sem_nulos = not df.isnull().any().any()

# 5. Validação da bateria inicial entre 0 e 100
validacao_bateria_inicial = df["bateria_inicial_pct"].between(0, 100).all()

# 6. Validação da bateria final entre 0 e 100
validacao_bateria_final = df["bateria_final_pct"].between(0, 100).all()

# 7. Validação: bateria final deve ser maior que a bateria inicial
validacao_bateria_ordem = (df["bateria_final_pct"] > df["bateria_inicial_pct"]).all()

# 8. Validação: variação de bateria deve ser positiva
validacao_variacao_bateria = (df["variacao_bateria_pct"] > 0).all()

# 9. Validação: energia consumida deve ser positiva
validacao_energia_positiva = (df["energia_consumida_kwh"] > 0).all()

# 10. Validação da potência média
validacao_potencia = df["potencia_media_kw"].between(22, 45).all()

# 11. Validação da duração da recarga
validacao_duracao = df["duracao_recarga_min"].between(5, 180).all()

# 12. Validação da ocupação do local
validacao_ocupacao = df["ocupacao_local_pct"].between(0, 100).all()

# 13. Validação da fila de espera
validacao_fila = df["fila_espera_min"].between(0, 60).all()

# 14. Validação da tarifa
validacao_tarifa = df["tarifa_kwh"].between(1.50, 4.00).all()

# 15. Validação do custo da energia
validacao_custo_energia = (df["custo_energia"] > 0).all()

# 16. Validação da taxa de serviço
validacao_taxa_servico = (df["taxa_servico"] > 0).all()

# 17. Validação do custo total
validacao_custo_total = (df["custo_total"] > 0).all()

# -------------------- Resultado das validações --------------------
validacoes = {
    "Quantidade mínima de linhas": validacao_linhas,
    "Quantidade mínima de colunas": validacao_colunas,
    "IDs únicos": validacao_ids_unicos,
    "Ausência de valores nulos": validacao_sem_nulos,
    "Bateria inicial entre 0 e 100": validacao_bateria_inicial,
    "Bateria final entre 0 e 100": validacao_bateria_final,
    "Bateria final maior que inicial": validacao_bateria_ordem,
    "Variação de bateria positiva": validacao_variacao_bateria,
    "Energia consumida positiva": validacao_energia_positiva,
    "Potência média entre 22 e 45 kW": validacao_potencia,
    "Duração entre 5 e 180 minutos": validacao_duracao,
    "Ocupação entre 0% e 100%": validacao_ocupacao,
    "Fila entre 0 e 60 minutos": validacao_fila,
    "Tarifa entre R$1,50 e R$4,00": validacao_tarifa,
    "Custo da energia positivo": validacao_custo_energia,
    "Taxa de serviço positiva": validacao_taxa_servico,
    "Custo total positivo": validacao_custo_total
}

for criterio, resultado in validacoes.items():
    status = "OK" if resultado else "FALHA"
    print(f"{criterio}: {status}")

base_aprovada = all(validacoes.values())

print("\nResultado final da validação:")
if base_aprovada:
    print("Base aprovada: todos os critérios de validação foram atendidos.")
else:
    print("Base reprovada: existem critérios que precisam ser revisados.")

# -------------------- Exportação da base --------------------
# Exporta a base em formato CSV
df.to_csv("base_recarga_veiculos_eletricos.csv", index=False, encoding="utf-8-sig")

print("\nResumo estatístico das principais variáveis numéricas:")
print(df[
    [
        "energia_consumida_kwh",
        "potencia_media_kw",
        "duracao_recarga_min",
        "ocupacao_local_pct",
        "fila_espera_min",
        "tarifa_kwh",
        "custo_energia",
        "taxa_servico",
        "custo_total"
    ]
].describe())

print("\n-------------------- CUSTO MÉDIO POR TIPO DE LOCAL --------------------")
custo_por_local = df.groupby("tipo_local")["custo_total"].mean().round(2)
print(custo_por_local)

print("\n-------------------- CUSTO MÉDIO POR CATEGORIA DE VEÍCULO --------------------")
custo_por_veiculo = df.groupby("categoria_veiculo")["custo_total"].mean().round(2)
print(custo_por_veiculo)

print("\n-------------------- CUSTO MÉDIO POR PERÍODO DO DIA --------------------")
custo_por_periodo = df.groupby("periodo_dia")["custo_total"].mean().round(2)
print(custo_por_periodo)

print("\n-------------------- 10 SESSÕES MAIS CARAS --------------------")
sessoes_mais_caras = df.sort_values(
    by="custo_total",
    ascending=False
).head(10)
print(sessoes_mais_caras[
    [
        "id_sessao",
        "tipo_local",
        "categoria_veiculo",
        "energia_consumida_kwh",
        "tarifa_kwh",
        "taxa_servico",
        "custo_total"
    ]
])
#Quanto maior a relação, maior influência uma na outra
print("\n-------------------- CORRELAÇÃO ENTRE VARIÁVEIS NUMÉRICAS --------------------")
correlacoes = df[
    [
        "capacidade_bateria_kwh",
        "variacao_bateria_pct",
        "energia_consumida_kwh",
        "potencia_media_kw",
        "duracao_recarga_min",
        "tarifa_kwh",
        "taxa_servico",
        "custo_total"
    ]
].corr().round(2)
print(correlacoes)

print("\n-------------------- VARIÁVEIS MAIS RELACIONADAS AO CUSTO TOTAL --------------------")
correlacao_custo = correlacoes["custo_total"].sort_values(ascending=False)
print(correlacao_custo)

print("\n-------------------- SIMULAÇÃO DE CENÁRIOS --------------------")
def calcular_custo_recarga(energia_consumida_kwh, tarifa_kwh, taxa_servico):
    custo_energia = energia_consumida_kwh * tarifa_kwh
    custo_total = custo_energia + taxa_servico
    return round(custo_total, 2)

cenario_baixo_custo = calcular_custo_recarga(
    energia_consumida_kwh=18,
    tarifa_kwh=1.80,
    taxa_servico=3.00
)

cenario_intermediario = calcular_custo_recarga(
    energia_consumida_kwh=38,
    tarifa_kwh=2.30,
    taxa_servico=5.00
)

cenario_alto_custo = calcular_custo_recarga(
    energia_consumida_kwh=65,
    tarifa_kwh=3.20,
    taxa_servico=8.00
)
print(f"Cenário de baixo custo: R$ {cenario_baixo_custo}")
print(f"Cenário intermediário: R$ {cenario_intermediario}")
print(f"Cenário de alto custo: R$ {cenario_alto_custo}")

print("\n-------------------- INTERPRETAÇÃO DOS RESULTADOS --------------------")
media_custo = df["custo_total"].mean()
media_energia = df["energia_consumida_kwh"].mean()
media_duracao = df["duracao_recarga_min"].mean()

local_maior_custo = custo_por_local.idxmax()
valor_maior_custo_local = custo_por_local.max()

veiculo_maior_custo = custo_por_veiculo.idxmax()
valor_maior_custo_veiculo = custo_por_veiculo.max()

print(f"O custo médio das sessões foi de R$ {media_custo:.2f}.")
print(f"A energia média consumida por sessão foi de {media_energia:.2f} kWh.")
print(f"A duração média das sessões foi de {media_duracao:.0f} minutos.")
print(f"O tipo de local com maior custo médio foi {local_maior_custo}, com média de R$ {valor_maior_custo_local:.2f}.")
print(f"A categoria de veículo com maior custo médio foi {veiculo_maior_custo}, com média de R$ {valor_maior_custo_veiculo:.2f}.")
