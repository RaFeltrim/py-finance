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

# Sidebar - Saldo Atual
st.sidebar.header("💼 Saldo Atual")
saldo_atual = obter_saldo()
novo_saldo = st.sidebar.number_input("Informe seu saldo disponível (R$)", value=saldo_atual, step=0.01, format="%.2f")
if st.sidebar.button("Atualizar Saldo"):
    atualizar_saldo(novo_saldo)
    st.sidebar.success("Saldo atualizado com sucesso!")
    st.rerun()

# Sidebar - Adicionar Transação
st.sidebar.header("Adicionar Transação")
with st.sidebar.form(key='nova_transacao', clear_on_submit=True):
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", step=0.01, format="%.2f")
    categoria = st.selectbox("Categoria", ["Entrada Fixa", "Entrada Variável", "Saída"], index=1)
    tags = {
        "Entrada Fixa": "💰 Entrada Fixa",
        "Entrada Variável": "🛅 Entrada Variável",
        "Saída": "💸 Saída"
    }
    st.caption(f"Categoria selecionada: {tags.get(categoria)}")
    datas = st.date_input("Data(s)", min_value=date.today() - timedelta(days=365))
    if isinstance(datas, date):
        datas = [datas]
    else:
        datas = sorted(datas)
    if len(datas) > 1:
        delta_dias = [(datas[i+1] - datas[i]).days for i in range(len(datas)-1)]
        consecutivos = all(delta == 1 for delta in delta_dias)
        if not consecutivos:
            st.warning("Selecione até 5 dias consecutivos.")
            datas = datas[:1]
        elif len(datas) > 5:
            st.warning("Selecione no máximo 5 dias consecutivos.")
            datas = datas[:5]
    submit = st.form_submit_button("Adicionar")
    if submit:
        if descricao and valor:
            if categoria == 'Saída':
                valor = -abs(valor)
            for d in datas:
                adicionar_transacao(d.strftime("%Y-%m-%d"), descricao, valor, categoria)
            st.success("Transação adicionada com sucesso!")
        else:
            st.error("Preencha todos os campos.")

# Chat de Entradas Rápidas
st.sidebar.header("Chat de Entradas Rápidas")
entrada_rapida = st.sidebar.text_area("Digite transações (ex: -50 ifood)")
if st.sidebar.button("Enviar Transações"):
    linhas = entrada_rapida.split('\n')
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) >= 2:
            valor = float(partes[0])
            descricao = ' '.join(partes[1:])
            categoria = 'Saída' if valor < 0 else 'Entrada Variável'
            adicionar_transacao(date.today().strftime("%Y-%m-%d"), f"[Diversos] {descricao}", valor, categoria)
    st.sidebar.success("Transações adicionadas!")

# Exibição de transações
df = obter_transacoes()
st.write("### 📋 Transações Registradas")

agrupados = df[df['Descrição'].str.startswith("[Diversos]")]
outros = df[~df['Descrição'].str.startswith("[Diversos]")]

for i, row in outros.iterrows():
    with st.expander(f"{row['Data'].date()} | {row['Descrição']} | R$ {row['Valor']:.2f}"):
        nova_desc = st.text_input(f"Descrição {row['ID']}", row['Descrição'], key=f"desc_{row['ID']}")
        novo_valor = st.number_input(f"Valor {row['ID']}", value=float(row['Valor']), step=0.01, key=f"valor_{row['ID']}")
        nova_cat = st.selectbox(f"Categoria {row['ID']}", ["Entrada Fixa", "Entrada Variável", "Saída"], index=["Entrada Fixa", "Entrada Variável", "Saída"].index(row['Categoria']), key=f"cat_{row['ID']}")
        col_edit, col_del = st.columns(2)
        if col_edit.button("Editar", key=f"edit_{row['ID']}"):
            editar_transacao(row['ID'], nova_desc, novo_valor, nova_cat)
            st.success("Transação editada!")
            st.rerun()
        if col_del.button("Remover", key=f"rem_{row['ID']}"):
            remover_transacao(row['ID'])
            st.error("Transação removida!")
            st.rerun()

if not agrupados.empty:
    with st.expander(f"💡 Diversos ({len(agrupados)} transações)"):
        for i, row in agrupados.iterrows():
            with st.container():
                nova_desc = st.text_input(f"Descrição {row['ID']}", row['Descrição'], key=f"desc_{row['ID']}")
                novo_valor = st.number_input(f"Valor {row['ID']}", value=float(row['Valor']), step=0.01, key=f"valor_{row['ID']}")
                nova_cat = st.selectbox(f"Categoria {row['ID']}", ["Entrada Fixa", "Entrada Variável", "Saída"], index=["Entrada Fixa", "Entrada Variável", "Saída"].index(row['Categoria']), key=f"cat_{row['ID']}")
                col_edit, col_del = st.columns(2)
                if col_edit.button("Editar", key=f"edit_div_{row['ID']}"):
                    editar_transacao(row['ID'], nova_desc, novo_valor, nova_cat)
                    st.success("Transação editada!")
                    st.rerun()
                if col_del.button("Remover", key=f"rem_div_{row['ID']}"):
                    remover_transacao(row['ID'])
                    st.error("Transação removida!")
                    st.rerun()

# Exportar Excel
if not df.empty:
    st.download_button("📅 Baixar Excel", data=to_excel(df), file_name="controle_financeiro.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Calendário
st.write("### 🗓️ Calendário Financeiro")
hoje = date.today()
mes_atual = hoje.month
ano_atual = hoje.year
cal = calendar.Calendar()
dias_mes = [d for d in cal.itermonthdates(ano_atual, mes_atual) if d.month == mes_atual]
df_mes = df[(df['Data'].dt.month == mes_atual) & (df['Data'].dt.year == ano_atual)]
agrupado = df_mes.groupby(df_mes['Data'].dt.date)['Valor'].sum()
agrupado = pd.to_numeric(agrupado, errors='coerce')
melhores_dias = agrupado[agrupado > 0].nlargest(5)

cores = []
valores = []
for dia in dias_mes:
    valor = agrupado.get(dia, 0)
    valores.append(valor)
    if valor > 0:
        if dia in melhores_dias:
            cores.append("lightblue")
        else:
            cores.append("lightgreen")
    elif valor < 0:
        cores.append("lightcoral")
    else:
        cores.append("white")

fig = go.Figure(data=[go.Bar(
    x=[d.strftime('%d/%m') for d in dias_mes],
    y=valores,
    marker_color=cores
)])
fig.update_layout(title=f"Resumo de {calendar.month_name[mes_atual]} {ano_atual}", xaxis_title="Dia", yaxis_title="Valor do Dia", height=400)
st.plotly_chart(fig, use_container_width=True)

# Recomendacão de gasto diário
dias_restantes = len([d for d in dias_mes if d >= hoje])
saldo_disponivel = saldo_atual
if dias_restantes > 0:
    gasto_recomendado = saldo_disponivel / dias_restantes
    st.info(f"💡 Valor recomendado para gastar por dia: R$ {gasto_recomendado:.2f}")

# Fechar conexão
conn.close()
