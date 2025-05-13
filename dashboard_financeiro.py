import streamlit as st
import pandas as pd
import altair as alt
import sqlite3
from datetime import date, timedelta, datetime
from io import BytesIO
import calendar
import plotly.graph_objects as go

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('financeiro.db')
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY,
    data TEXT,
    descricao TEXT,
    valor REAL,
    categoria TEXT
)
''')

# Criar tabela de saldo
c.execute('''
CREATE TABLE IF NOT EXISTS saldo (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    valor REAL
)
''')
conn.commit()

# Funções para saldo
def obter_saldo():
    c.execute('SELECT valor FROM saldo WHERE id = 1')
    resultado = c.fetchone()
    return resultado[0] if resultado else 0.0

def atualizar_saldo(valor):
    if c.execute('SELECT 1 FROM saldo WHERE id = 1').fetchone():
        c.execute('UPDATE saldo SET valor = ? WHERE id = 1', (valor,))
    else:
        c.execute('INSERT INTO saldo (id, valor) VALUES (1, ?)', (valor,))
    conn.commit()

def atualizar_saldo_automatico():
    hoje = date.today().strftime("%Y-%m-%d")
    c.execute('''
    SELECT valor, data FROM transacoes
    WHERE data <= ? AND categoria IN ('Entrada Fixa', 'Entrada Variável')
    ''', (hoje,))
    entradas_nao_processadas = c.fetchall()

    total_entradas = sum([entrada[0] for entrada in entradas_nao_processadas])

    if total_entradas != 0:
        saldo_atual = obter_saldo()
        novo_saldo = saldo_atual + total_entradas
        atualizar_saldo(novo_saldo)

# Funções de transações
def adicionar_transacao(data, descricao, valor, categoria):
    c.execute('''
    INSERT INTO transacoes (data, descricao, valor, categoria)
    VALUES (?, ?, ?, ?)
    ''', (data, descricao, valor, categoria))
    conn.commit()

def obter_transacoes():
    c.execute('''
    SELECT id, data, descricao, valor, categoria FROM transacoes
    ORDER BY data
    ''')
    dados = c.fetchall()
    df = pd.DataFrame(dados, columns=["ID", "Data", "Descrição", "Valor", "Categoria"])
    df['Data'] = pd.to_datetime(df['Data'])
    return df

def calcular_saldo_total_esperado(saldo_atual, transacoes, data_final):
    transacoes['Data'] = pd.to_datetime(transacoes['Data'])
    hoje = pd.Timestamp(date.today())
    data_final = pd.Timestamp(data_final)
    futuras_transacoes = transacoes[transacoes['Data'] > hoje]
    saldo_futuro = futuras_transacoes[transacoes['Data'] <= data_final]['Valor'].sum()
    return saldo_atual + saldo_futuro

def calcular_saldo_fechamento_mes(saldo_atual):
    hoje = date.today()
    ultimo_dia_mes = date(hoje.year, hoje.month, calendar.monthrange(hoje.year, hoje.month)[1])
    dias_do_mes = pd.date_range(start=hoje, end=ultimo_dia_mes)

    saldo_estimado = saldo_atual
    for dia in dias_do_mes:
        if dia.weekday() == 1:  # Terça-feira
            saldo_estimado += 50
        elif dia.weekday() == 6:  # Domingo
            saldo_estimado += 60
        elif dia.weekday() in [3, 4, 5]:  # Quinta a Sábado
            saldo_estimado += 80

    return saldo_estimado

def editar_transacao(id, nova_descricao, novo_valor, nova_categoria):
    c.execute('''
    UPDATE transacoes
    SET descricao = ?, valor = ?, categoria = ?
    WHERE id = ?
    ''', (nova_descricao, novo_valor, nova_categoria, id))
    conn.commit()

def remover_transacao(id):
    c.execute('DELETE FROM transacoes WHERE id = ?', (id,))
    conn.commit()

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df['Data'] = pd.to_datetime(df['Data'])
        for (ano, mes), grupo in df.groupby([df['Data'].dt.year, df['Data'].dt.month]):
            nome_aba = f"{calendar.month_name[mes]}_{ano}"
            grupo.to_excel(writer, sheet_name=nome_aba, index=False)
    return output.getvalue()

# Interface Streamlit
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro")

# Atualizar saldo automaticamente com base nas entradas previstas para o dia atual ou anteriores
atualizar_saldo_automatico()

# Sidebar - Saldo Atual
st.sidebar.header("💼 Saldo Atual")
saldo_atual = obter_saldo()
novo_saldo = st.sidebar.number_input("Informe seu saldo disponível (R$)", value=saldo_atual, step=0.01, format="%.2f")
if st.sidebar.button("Atualizar Saldo"):
    atualizar_saldo(novo_saldo)
    st.sidebar.success("Saldo atualizado com sucesso!")
    st.experimental_rerun()

# Exibir Saldos no Topo
transacoes = obter_transacoes()
ultimo_dia_mes = date(date.today().year, date.today().month, calendar.monthrange(date.today().year, date.today().month)[1])
saldo_total_esperado = calcular_saldo_total_esperado(saldo_atual, transacoes, ultimo_dia_mes)
saldo_fechamento_mes = calcular_saldo_fechamento_mes(saldo_atual)

col1, col2, col3 = st.columns(3)
col1.metric("Saldo Total (Atual)", f"R$ {saldo_atual:.2f}")
col2.metric("Saldo Total Esperado (Fim do Mês)", f"R$ {saldo_total_esperado:.2f}")
col3.metric("Saldo no Fechamento do Mês", f"R$ {saldo_fechamento_mes:.2f}")

# Sidebar - Adicionar Transação
st.sidebar.header("Adicionar Transação")
with st.sidebar.form(key='nova_transacao', clear_on_submit=True):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", step=0.01, format="%.2f")
    categoria = st.selectbox("Categoria", ["Entrada Fixa", "Entrada Variável", "Saída"], index=1)
    datas = st.date_input("Data(s)", min_value=date.today() - timedelta(days=365))
    if isinstance(datas, date):
        datas = [datas]
    submit = st.form_submit_button("Adicionar")
    if submit:
        if descricao and valor:
            valor = -abs(valor) if categoria == 'Saída' else valor
            for d in datas:
                adicionar_transacao(d.strftime("%Y-%m-%d"), descricao, valor, categoria)
            st.success("Transação adicionada com sucesso!")
        else:
            st.error("Preencha todos os campos.")

# Exibição de transações
df = obter_transacoes()
st.write("### 📋 Transações Registradas")
st.dataframe(df)

# Exportar Excel
if not df.empty:
    st.download_button("📅 Baixar Excel", data=to_excel(df), file_name="controle_financeiro.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Recomendação de gasto diário
dias_restantes = len([d for d in pd.date_range(start=pd.Timestamp(date.today()), end=ultimo_dia_mes) if d >= pd.Timestamp(date.today())])
gasto_recomendado = saldo_atual / dias_restantes if dias_restantes > 0 else 0
st.info(f"💡 Valor recomendado para gastar por dia: R$ {gasto_recomendado:.2f}")

# Fechar conexão
conn.close()