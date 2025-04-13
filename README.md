# 📊 Dashboard Financeiro

Este projeto é um dashboard financeiro interativo desenvolvido com **Streamlit**, que permite gerenciar entradas, saídas e transações financeiras de forma prática e intuitiva. O sistema utiliza um banco de dados SQLite para armazenar informações sobre transações e saldo, além de integrar gráficos e funcionalidades de calendário para visualização e controle.

## 🎯 Objetivo

O objetivo deste dashboard é fornecer uma ferramenta simples e eficiente para acompanhar suas finanças, criando uma visão clara sobre suas entradas e saídas, bem como calcular o saldo atual e propor recomendações de gastos diários.

---

## 💻 Funcionalidades

### **1. Gerenciamento de Saldo**
- Visualize e atualize o saldo disponível diretamente na barra lateral.
- Saldo é armazenado de forma persistente no banco de dados SQLite.

### **2. Registro de Transações**
- Registre novas transações de entrada (fixa ou variável) ou saída.
- Adicione transações para uma ou mais datas consecutivas (até 5 dias).
- Possibilidade de categorizar cada transação:
  - **💰 Entrada Fixa**
  - **🛅 Entrada Variável**
  - **💸 Saída**
- Edição e exclusão de transações diretamente no dashboard.

### **3. Chat de Entradas Rápidas**
- Registre múltiplas transações rapidamente com o formato:
  ```
  <valor> <descrição>
  Exemplo:
  -50 ifood
  100 salário
  ```
- As transações serão automaticamente categorizadas como **Entrada Variável** (valores positivos) ou **Saída** (valores negativos).

### **4. Visualização de Transações**
- Visualize todas as transações registradas em uma tabela interativa.
- As transações podem ser editadas ou removidas diretamente.

### **5. Exportação para Excel**
- Exporte todas as transações registradas para um arquivo Excel.
- Cada mês é salvo em uma aba separada no Excel.

### **6. Calendário Financeiro**
- Exibe um resumo visual das transações em formato de calendário.
- Os dias com transações positivas aparecem em verde ou azul claro (melhores dias), enquanto os dias negativos aparecem em vermelho.
- Gráfico de barras com os valores diários do mês atual.

### **7. Recomendação de Gasto Diário**
- Com base no saldo disponível e nos dias restantes do mês, o sistema calcula e exibe um valor recomendado para gastar por dia.

---

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/):** Framework para criação de aplicativos web interativos em Python.
- **[SQLite](https://www.sqlite.org/):** Banco de dados relacional leve e embutido para armazenamento persistente.
- **[Pandas](https://pandas.pydata.org/):** Biblioteca de manipulação e análise de dados.
- **[Plotly](https://plotly.com/python/):** Criação de gráficos interativos.
- **[Altair](https://altair-viz.github.io/):** Criação de gráficos declarativos e interativos.

---

## 📦 Estrutura do Projeto

- **`financeiro.db`:** Banco de dados SQLite para armazenar informações de saldo e transações.
- **`dashboard_financeiro.py`:** Código principal do dashboard.
- **Gráficos e Visualizações:** Integrados ao dashboard com Plotly e Altair.

---

## 🚀 Como Utilizar

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie um Ambiente Virtual (opcional):**
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o Dashboard:**
   ```bash
   streamlit run dashboard_financeiro.py
   ```

5. **Acesse no Navegador:**
   O Streamlit abrirá automaticamente no navegador. Caso contrário, acesse:
   ```
   http://localhost:8501
   ```

---

## 📈 Funcionalidades Futuras

- **Integração com APIs Bancárias:**
  Automatizar o registro de transações a partir de dados de bancos ou fintechs.
- **Análise Preditiva:**
  Utilizar machine learning para prever despesas e receitas futuras.
- **Gráficos Avançados:**
  Implementar novos gráficos para análise detalhada de categorias e tendências.
- **Alertas Personalizados:**
  Notificar o usuário sobre orçamento excedido ou metas atingidas.

---

## 🚧 Limitações Conhecidas

- **Número de Datas Consecutivas:** É permitido registrar transações para no máximo 5 dias consecutivos.
- **Persistência do Banco de Dados:** O banco de dados SQLite é armazenado localmente, não sendo ideal para múltiplos usuários.
- **Interface:** Algumas funcionalidades podem ser otimizadas para dispositivos móveis.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias ou novas funcionalidades.

1. **Fork este repositório.**
2. Crie um branch com sua feature:
   ```bash
   git checkout -b nova-feature
   ```
3. Faça o commit das alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade X"
   ```
4. Envie seu branch:
   ```bash
   git push origin nova-feature
   ```
5. Abra um Pull Request.