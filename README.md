# 🛰️ OrbitHub - Satellite Data Marketplace

[![NASA Hackathon 2025](https://img.shields.io/badge/NASA-Hackathon%202025-blue)](https://www.spaceappschallenge.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)

**OrbitHub** é uma plataforma inovadora de marketplace de dados de satélites desenvolvida para o NASA Space Apps Challenge 2025. A plataforma classifica satélites baseado em critérios de sustentabilidade ambiental usando Machine Learning e oferece um portal bilíngue (EN/PT) para solicitação de dados.

![OrbitHub Screenshot](https://via.placeholder.com/800x400/0a1628/00d1ff?text=OrbitHub+Portal)

## 🌟 **Características Principais**

### 🤖 **Machine Learning**
- **Classificação Automática**: Algoritmo KMeans que classifica satélites em três categorias de sustentabilidade
  - 🥇 **OURO/GOLD**: Satélites com alto grau de sustentabilidade
  - 🥈 **PRATA/SILVER**: Satélites com grau médio de sustentabilidade
  - 🥉 **BRONZE**: Satélites com grau básico de sustentabilidade

### 🌍 **Portal Bilíngue**
- Interface completa em **Inglês** e **Português**
- Tradução automática de todos os elementos da UI
- Classificação dos satélites traduzida dinamicamente

### 🎨 **UI/UX Futurista**
- Design dark mode com efeitos neon
- Animações espaciais de fundo
- Interface responsiva e moderna
- Tooltips informativos em todos os campos

### 📊 **Funcionalidades do Portal**

#### 👥 **Cadastro de Cliente**
- Nome completo
- CNPJ (Company ID)
- Endereço
- Email
- Ramo de atividade (Business Sector)
- País (195+ países disponíveis)

#### 🔍 **Filtros de Busca**
- **Finalidade**: 40+ categorias (Earth Observation, Communications, Space Science, etc.)
- **Classificação Ecológica**: OURO/GOLD, PRATA/SILVER, BRONZE
- **Tipo de Entrega**: API ou Batch

#### ✅ **Seleção Múltipla de Satélites**
- Checkboxes em cada satélite
- Indicador visual de seleção (borda neon)
- Contador de satélites selecionados

#### 📄 **Relatórios Detalhados**
Cada solicitação gera um arquivo TXT com:
- Informações completas do cliente
- Detalhes da solicitação
- Lista de satélites selecionados com:
  - Nome do satélite
  - Nomes alternativos
  - País de registro na ONU
  - País do operador
  - Proprietário/Operador
  - Finalidade
  - Finalidade detalhada
  - Classificação ecológica

---

## 🚀 **Instalação e Execução**

### **Pré-requisitos**

- Python 3.11+
- Node.js 18+
- npm ou yarn

### **1. Clone o Repositório**

```bash
git clone https://github.com/anibalssilva/OrbitHub.git
cd OrbitHub
```

### **2. Configuração do Backend**

```bash
# Navegue para a pasta backend
cd backend

# Instale as dependências
pip install -r requirements.txt

# Treine o modelo ML (primeira execução)
python -m app.train

# Classifique os satélites
python -m app.predict

# Inicie o servidor FastAPI
python -m uvicorn app.main:app --port 8000 --reload
```

O backend estará disponível em: `http://localhost:8000`

### **3. Configuração do Frontend**

```bash
# Em outro terminal, navegue para a pasta frontend
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev -- --host --port 5173
```

O frontend estará disponível em: `http://localhost:5173`

### **4. Acesse a Aplicação**

- **Homepage**: `http://localhost:5173/`
- **Portal de Requisições**: `http://localhost:5173/portal.html`
- **API Docs**: `http://localhost:8000/docs`

---

## 📁 **Estrutura do Projeto**

```
OrbitHub/
├── backend/                      # Backend FastAPI + ML
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # API FastAPI
│   │   ├── data_access.py       # Acesso aos dados
│   │   ├── features.py          # Feature engineering
│   │   ├── train.py             # Treinamento do modelo
│   │   ├── predict.py           # Predição e classificação
│   │   └── models/              # Modelos ML treinados
│   │       ├── kmeans.joblib
│   │       ├── preprocessor.joblib
│   │       └── cluster_label_map.json
│   ├── data/
│   │   ├── raw/                 # Dados brutos
│   │   │   └── UCS-Satellite-Database 5-1-2023.xlsx
│   │   └── processed/           # Dados processados
│   │       ├── satellites_classified.csv
│   │       └── portal_requests.jsonl
│   ├── solicitacoes/            # Relatórios TXT gerados
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                     # Frontend React + Vite
│   ├── src/
│   │   ├── portal/
│   │   │   ├── App.jsx          # Componente principal
│   │   │   └── style.css        # Estilos do portal
│   │   └── main.jsx             # Entry point
│   ├── index.html               # Homepage
│   ├── portal.html              # Portal de requisições
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── README.md
├── START_SERVERS.md             # Guia de inicialização
└── LICENSE

```

---

## 🔌 **API Endpoints**

### **1. Health Check**
```http
GET /health
```
Verifica se a API está funcionando.

**Response:**
```json
{
  "status": "ok"
}
```

### **2. Listar Satélites**
```http
GET /satellites?classification={OURO|PRATA|BRONZE}&purpose={string}&delivery={API|Batch}&limit={number}
```

**Parâmetros de Query:**
- `classification` (opcional): Filtrar por classificação ecológica
- `purpose` (opcional): Filtrar por finalidade
- `delivery` (opcional): Tipo de entrega
- `limit` (padrão: 50): Número máximo de resultados

**Response:**
```json
[
  {
    "name_of_satellite": "USA 288",
    "alternate_names": "AEHF-4 (Advanced Extremely High Frequency satellite-4, USA 288)",
    "country_un_registry": "USA",
    "country_operator_owner": "USA",
    "operator_owner": "US Air Force",
    "purpose": "Communications",
    "detailed_purpose": "Military Communications",
    "sustainability_class": "BRONZE"
  }
]
```

### **3. Enviar Solicitação**
```http
POST /portal/request
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "João Silva",
  "cnpj": "12.345.678/0001-90",
  "address": "Rua das Flores, 123",
  "email": "joao@empresa.com.br",
  "sector": "Scientific",
  "country": "Brazil",
  "purpose": "Communications",
  "purposeOther": "",
  "classification": "BRONZE",
  "delivery": "API",
  "description": "Dados para pesquisa acadêmica",
  "language": "pt",
  "selected_satellites": [
    {
      "name_of_satellite": "USA 288",
      "sustainability_class": "BRONZE",
      ...
    }
  ]
}
```

**Response:**
```json
{
  "status": "received",
  "path": "solicitacoes/solicitacao_João_Silva_20251004_200250.txt"
}
```

---

## 🧠 **Machine Learning**

### **Modelo de Classificação**

O sistema usa **K-Means clustering** com as seguintes features:

#### **Features Numéricas:**
- `LIFETIME_YEARS`: Tempo de vida útil do satélite (quanto maior, mais sustentável)
- `CAPABILITIES_COUNT`: Número de capacidades/funções (mais funções = maior sustentabilidade)

#### **Features Categóricas:**
- `PURPOSE`: Finalidade do satélite (satélites ambientais têm maior score)
- `OPS_STATUS_CODE`: Status operacional

#### **Critérios de Sustentabilidade:**

1. **Impacto Ambiental** (`ENV_IMPACT_SCORE`):
   - Satélites de observação da Terra, ciência climática, e meteorologia recebem scores altos
   - Satélites militares recebem scores mais baixos

2. **Tempo de Vida**:
   - Satélites com maior tempo de vida são mais sustentáveis (menos lixo espacial)

3. **Multifuncionalidade**:
   - Satélites com múltiplas capacidades são mais eficientes

### **Pipeline de Treinamento**

1. **Feature Engineering**: Cálculo de métricas de sustentabilidade
2. **Preprocessing**: Normalização e encoding de features
3. **Clustering**: KMeans com 3 clusters
4. **Labeling**: Mapeamento dos clusters para OURO, PRATA, BRONZE

---

## 🌐 **Deployment**

### **Backend (Railway/Render/Heroku)**

1. Configure as variáveis de ambiente
2. Instale as dependências: `pip install -r backend/requirements.txt`
3. Execute as migrações e treinamento do modelo
4. Inicie o servidor: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### **Frontend (Vercel/Netlify)**

1. Build: `npm run build`
2. Configure a pasta de output: `dist/`
3. Configure rewrites para SPAs

---

## 🤝 **Contribuindo**

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 **Licença**

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 **Equipe**

Desenvolvido para o **NASA Space Apps Challenge 2025**

- **GitHub**: [@anibalssilva](https://github.com/anibalssilva)
- **Repositório**: [OrbitHub](https://github.com/anibalssilva/OrbitHub)

---

## 🙏 **Agradecimentos**

- **NASA** por disponibilizar os dados do UCS Satellite Database
- **Space Apps Challenge** pela oportunidade
- Comunidade open-source

---

## 📧 **Contato**

Para dúvidas ou sugestões, abra uma [issue](https://github.com/anibalssilva/OrbitHub/issues) no GitHub.

---

<div align="center">
  
**🌟 Se você gostou deste projeto, dê uma estrela! 🌟**

Made with ❤️ for a sustainable space future 🛰️

</div>
