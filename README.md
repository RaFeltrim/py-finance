# 📊 Dashboard Financeiro

Este é um dashboard financeiro interativo desenvolvido com Streamlit, que permite gerenciar entradas, saídas e transações financeiras de forma prática e intuitiva. O sistema utiliza um banco de dados SQLite para armazenar informações sobre transações e saldo, além de integrar gráficos e funcionalidades de calendário para visualização e controle.

---

## 🎯 Objetivo

Fornecer uma ferramenta simples e eficiente para acompanhar suas finanças, oferecendo:

- Visão clara de entradas e saídas  
- Cálculo automático do saldo atual  
- Recomendação de gasto diário com base no saldo disponível  

---

## 💻 Funcionalidades

1. **Gerenciamento de Saldo**  
   - Visualize e atualize o saldo disponível na barra lateral.  
   - Saldo armazenado de forma persistente no banco de dados SQLite.

2. **Registro de Transações**  
   - Adicione novas transações de entrada (fixa ou variável) ou saída.  
   - Pode registrar para até 5 dias consecutivos.  
   - Categorize cada transação:  
     - 💰 Entrada Fixa  
     - 🛅 Entrada Variável  
     - 💸 Saída  
   - Edite ou exclua transações diretamente no dashboard.

3. **Chat de Entradas Rápidas**  
   - Registre várias transações de uma vez usando o formato:  
     ```
     <valor> <descrição>
     ```  
     Exemplo:
     ```
     -50 ifood
     100 salário
     ```  
   - O sistema identifica automaticamente se é Entrada Variável (positivo) ou Saída (negativo).

4. **Visualização de Transações**  
   - Tabela interativa com todas as transações.  
   - Edição e remoção inline.

5. **Exportação para Excel**  
   - Exporte todas as transações em um arquivo `.xlsx`.  
   - Cada mês gera uma aba separada.

6. **Calendário Financeiro**  
   - Resumo visual das transações em formato de calendário.  
   - Dias com saldo positivo em verde/azul claro; negativos em vermelho.  
   - Gráfico de barras mostrando valores diários do mês atual.

7. **Recomendação de Gasto Diário**  
   - Calcula valor recomendado de gasto por dia com base no saldo e dias restantes do mês.

---

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: criação de interface web interativa  
- **SQLite**: banco de dados leve e embutido  
- **Pandas**: manipulação e análise de dados  
- **Plotly & Altair**: gráficos interativos e declarativos  
- **Python 3.10**  

---

## 📦 Estrutura do Projeto

```
├── dashboard_financeiro.py  # Aplicação Streamlit principal
├── financeiro.db            # Banco de dados SQLite
├── requirements.txt         # Dependências Python
├── Dockerfile               # Configuração de container Docker
└── README.md                # Documentação e instruções
```

---

## 🚀 Como Utilizar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. [Opcional] Criar ambiente virtual
```bash
python -m venv env
# Linux/Mac
source env/bin/activate
# Windows
env\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar localmente (sem Docker)
```bash
streamlit run dashboard_financeiro.py
```

Acesse no navegador:

```
http://localhost:8501
```

---

### 🐳 Uso com Docker

Este projeto inclui um Dockerfile para facilitar a implantação:

#### 1. Build da imagem
```bash
docker build -t py-finance .
```

#### 2. Executar o container
```bash
docker run --rm -p 8501:8501 \
  -v /caminho/para/dados:/app/data \
  py-finance
```

- `-p 8501:8501`: mapeia a porta 8501 do container para sua máquina.
- `-v /caminho/para/dados:/app/data`: monta uma pasta local para leitura/gravação de arquivos (opcional).

#### 3. Acessar no navegador
```
http://localhost:8501
```

---

## 📈 Funcionalidades Futuras

- **Integração com APIs Bancárias**: importar transações automaticamente
- **Análise Preditiva**: usar ML para prever receitas e despesas
- **Gráficos Avançados**: filtragem por categoria, tendências de longo prazo
- **Alertas Personalizados**: notificações de orçamento excedido ou metas alcançadas

---

## 🚧 Limitações Conhecidas

- Registro limitado a 5 dias consecutivos por transação em lote.
- Banco SQLite local não ideal para múltiplos usuários simultâneos.
- Responsividade móvel ainda pode ser aprimorada.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para colaborar:

1. Faça um fork do repositório
2. Crie um branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Adiciona feature X"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin feature/nome-da-feature
   ```
5. Abra um Pull Request