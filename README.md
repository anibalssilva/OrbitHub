# 🛰️ OrbitHub

<div align="center">

![OrbitHub Banner](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge%202025-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Satellite Sustainability Marketplace powered by Machine Learning**

*Democratizing access to eco-classified satellite data for a smarter, greener planet* 🌍

[English](#english) | [Português](#português)

</div>

---

## English

### 🌟 **Overview**

**OrbitHub** is an innovative ML-powered platform that classifies satellites based on sustainability criteria and provides an intuitive bilingual portal (EN/PT) for clients to request satellite data. Developed for the **NASA Space Apps Challenge 2025**, OrbitHub addresses the critical need for environmental impact assessment in space missions.

### 🎯 **Problem Statement**

With over **5,000 active satellites** orbiting Earth, understanding their environmental footprint is crucial for:
- 🌱 Reducing space debris
- ♻️ Promoting sustainable space missions
- 📊 Informed decision-making for satellite operators
- 🔍 Transparent sustainability reporting

### 💡 **Solution**

OrbitHub introduces a **3-tier sustainability classification system** (GOLD 🥇 / SILVER 🥈 / BRONZE 🥉) using **unsupervised machine learning (KMeans clustering)** based on:

| **Criterion** | **Weight** | **Description** |
|--------------|-----------|----------------|
| 🎯 **Purpose Alignment** | 40% | Environmental/Earth observation missions score higher |
| ⏰ **Lifetime** | 30% | Longer operational life = better resource utilization |
| 🔧 **Capabilities** | 20% | Multi-functional satellites are more efficient |
| 🌍 **Environmental Impact** | 10% | Lower orbital parameters = reduced debris risk |

---

### 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React + Vite)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Homepage   │  │  Portal Form │  │  Satellite Catalog   │  │
│  │  (index.html)│  │  (React SPA) │  │  (Filtered Results)  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
│         └─────────────────┴──────────────────────┘              │
│                           │ HTTP/JSON                           │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                           ▼ BACKEND (FastAPI)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   API ENDPOINTS                           │  │
│  │  • GET  /health         - Health check                   │  │
│  │  • POST /classify       - Individual classification      │  │
│  │  • GET  /satellites     - Filtered catalog               │  │
│  │  • POST /portal/request - Client data request            │  │
│  └─────────────────────┬────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────┴────────────────────────────────────┐  │
│  │              DATA ACCESS LAYER                            │  │
│  │  • filter_satellites() - Query & filter logic            │  │
│  │  • persist_portal_request() - Save requests              │  │
│  └─────────────────────┬────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────┴────────────────────────────────────┐  │
│  │              MACHINE LEARNING PIPELINE                    │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │  Preprocessor (ColumnTransformer)                │    │  │
│  │  │  • Numeric: Imputer → StandardScaler             │    │  │
│  │  │  • Categorical: Imputer → OneHotEncoder          │    │  │
│  │  └─────────────┬────────────────────────────────────┘    │  │
│  │                │                                           │  │
│  │  ┌─────────────▼────────────────────────────────────┐    │  │
│  │  │  KMeans Clustering (n_clusters=3)                │    │  │
│  │  │  Cluster 0 → GOLD   (Highest sustainability)    │    │  │
│  │  │  Cluster 1 → SILVER (Medium sustainability)      │    │  │
│  │  │  Cluster 2 → BRONZE (Lower sustainability)       │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                           ▼ DATA LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  data/raw/                                                │  │
│  │  └── UCS-Satellite-Database-5-1-2023.xlsx                │  │
│  │                                                            │  │
│  │  data/processed/                                          │  │
│  │  ├── satellites_classified.csv (Cached classifications)  │  │
│  │  └── portal_requests.jsonl (Request log)                 │  │
│  │                                                            │  │
│  │  solicitacoes/                                            │  │
│  │  └── solicitacao_ClientName_YYYYMMDD_HHMMSS.txt          │  │
│  │      (Human-readable bilingual reports)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🚀 **Features**

#### **🔍 Satellite Classification**
- ✅ **KMeans clustering** with 3 sustainability tiers
- ✅ **Automated feature engineering** from UCS Satellite Database
- ✅ **Composite scoring** algorithm (purpose + lifetime + capabilities + impact)
- ✅ **Cache-enabled** for fast API responses

#### **🌐 Bilingual Portal (EN/PT)**
- ✅ **Dynamic language switching** (English/Portuguese)
- ✅ **40+ satellite purposes** (Earth Observation, Communications, etc.)
- ✅ **195+ countries** supported in client registration
- ✅ **Multi-satellite selection** with checkbox interface
- ✅ **Real-time filtering** by sustainability class & purpose

#### **📋 Client Request Management**
- ✅ **Comprehensive client data** collection (name, company ID, sector, country)
- ✅ **Flexible delivery options** (API / Batch)
- ✅ **Bilingual reports** generation (TXT format)
- ✅ **JSONL logging** for request analytics

#### **🎨 Modern UI/UX**
- ✅ **Futuristic dark theme** with neon accents
- ✅ **Responsive design** (mobile/tablet/desktop)
- ✅ **Animated space canvas** background
- ✅ **Tooltip-based help system** for all form fields

---

### 📊 **Machine Learning Details**

#### **Input Features**
```python
{
    "PURPOSE": str,              # Categorical: mission purpose
    "OPS_STATUS_CODE": str,      # Categorical: operational status
    "LIFETIME_YEARS": float,     # Numeric: mission lifespan
    "CAPABILITIES_COUNT": int,   # Numeric: number of functions
    "ENV_IMPACT_SCORE": float    # Numeric: orbital debris risk
}
```

#### **Preprocessing Pipeline**
```python
ColumnTransformer([
    ("numeric", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), ["LIFETIME_YEARS", "CAPABILITIES_COUNT", "ENV_IMPACT_SCORE"]),
    
    ("categorical", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), ["PURPOSE", "OPS_STATUS_CODE"])
])
```

#### **Cluster-to-Label Mapping**
```python
# Composite score calculation
composite_score = (
    0.4 * purpose_alignment +
    0.3 * normalized_lifetime +
    0.2 * normalized_capabilities +
    0.1 * (1 - normalized_env_impact)
)

# Clusters sorted by mean composite score (descending)
# Highest score → GOLD, Medium → SILVER, Lowest → BRONZE
```

---

### 🛠️ **Tech Stack**

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite 5 | SPA with hot-reload |
| **Backend** | FastAPI 0.110+ | Async REST API |
| **ML** | scikit-learn 1.3+ | KMeans clustering |
| **Data** | pandas + openpyxl | Data processing |
| **Server** | Uvicorn | ASGI server |
| **Styling** | Custom CSS | Futuristic UI |

---

### 📦 **Installation & Setup**

#### **Prerequisites**
- Python 3.11+
- Node.js 18+
- npm/yarn

#### **1. Clone Repository**
```bash
git clone https://github.com/anibalssilva/OrbitHub.git
cd OrbitHub
```

#### **2. Backend Setup**
```powershell
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Train the ML model (first time only)
python -m app.train

# Generate initial classifications
python -m app.predict

# Start the API server
python -m uvicorn app.main:app --port 8000 --reload
```

✅ **Backend running on:** `http://localhost:8000`  
📄 **API Docs:** `http://localhost:8000/docs`

#### **3. Frontend Setup**
```powershell
# Navigate to frontend directory (from project root)
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev -- --host --port 5173
```

✅ **Frontend running on:** `http://localhost:5173`

#### **4. Access the Application**
- **Homepage:** http://localhost:5173/
- **Portal:** http://localhost:5173/portal.html
- **API Docs:** http://localhost:8000/docs

---

### 📁 **Project Structure**

```
OrbitHub/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & endpoints
│   │   ├── data_access.py       # Data loading & filtering logic
│   │   ├── features.py          # Feature engineering functions
│   │   ├── train.py             # ML model training script
│   │   ├── predict.py           # Classification prediction script
│   │   └── models/              # Saved ML artifacts
│   │       ├── kmeans.joblib
│   │       ├── preprocessor.joblib
│   │       ├── cluster_label_map.json
│   │       └── feature_defaults.json
│   ├── requirements.txt         # Python dependencies
│   └── pyproject.toml           # Project metadata
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── main.jsx             # React entry point
│   │   └── portal/
│   │       ├── App.jsx          # Main portal component
│   │       └── style.css        # Futuristic styling
│   ├── index.html               # Homepage (pure HTML/CSS/JS)
│   ├── portal.html              # Portal entry point
│   ├── package.json             # Node dependencies
│   └── vercel.json              # Vercel deployment config
├── data/
│   ├── raw/
│   │   └── UCS-Satellite-Database-5-1-2023.xlsx  # Source data
│   └── processed/
│       ├── satellites_classified.csv             # ML output
│       └── portal_requests.jsonl                 # Request log
├── solicitacoes/                # Client request reports (TXT)
├── docs/                        # Additional documentation
├── .gitignore
├── LICENSE                      # MIT License
├── README.md                    # This file
├── DEPLOYMENT.md                # Deployment guide
├── START_SERVERS.md             # Quick start guide
└── requirements.txt             # Root Python dependencies
```

---

### 🌐 **API Endpoints**

#### **GET /health**
Health check endpoint.
```json
{ "status": "ok" }
```

#### **POST /classify**
Classify individual satellites.
```json
// Request
[{
  "PURPOSE": "Earth Observation",
  "LIFETIME_YEARS": 15.0,
  "CAPABILITIES_COUNT": 5
}]

// Response
[{ "label": "OURO" }]
```

#### **GET /satellites**
Get filtered satellite catalog.
```
GET /satellites?classification=OURO&purpose=Communications&limit=24

// Response
[{
  "name_of_satellite": "ISS (ZARYA)",
  "alternate_names": "International Space Station",
  "country_un_registry": "USA",
  "country_operator_owner": "USA",
  "operator_owner": "NASA",
  "purpose": "Earth Observation",
  "detailed_purpose": "Crewed space station",
  "sustainability_class": "OURO"
}]
```

#### **POST /portal/request**
Submit client data request.
```json
// Request
{
  "name": "Client Name",
  "email": "client@example.com",
  "country": "Brazil",
  "purpose": "Earth Observation",
  "classification": "OURO",
  "delivery": "API",
  "selected_satellites": [...],
  "language": "pt"
}

// Response
{
  "status": "received",
  "path": "solicitacoes/solicitacao_Client_Name_20251004_120000.txt"
}
```

---

### 🎨 **UI Screenshots**

*(Screenshots would be added here)*

#### Homepage
- Hero section with animated space background
- Language switcher (EN/PT)
- Call-to-action button to portal

#### Request Portal
- Client information form (6 fields)
- Request details with dropdowns
- Real-time satellite filtering
- Multi-select with checkboxes
- Submit with bilingual success message

#### Satellite Cards
- Name & alternate names
- Sustainability badge (color-coded)
- Country, operator, purpose details
- Selection checkbox

---

### 🚀 **Deployment**

#### **Option 1: Railway (Backend)**
1. Sign up at https://railway.app
2. Connect GitHub repository
3. Set root directory: `backend/`
4. Configure build command:
   ```bash
   pip install -r requirements.txt && python -m app.train && python -m app.predict
   ```
5. Set start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

#### **Option 2: Vercel (Frontend)**
1. Sign up at https://vercel.com
2. Import Git repository
3. Set root directory: `frontend/`
4. Framework preset: Vite
5. Add environment variable:
   - `VITE_API_URL`: Your Railway backend URL

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

---

### 📝 **Usage Example**

```python
# Example: Classify a new satellite
import requests

payload = {
    "PURPOSE": "Communications",
    "LIFETIME_YEARS": 10.0,
    "CAPABILITIES_COUNT": 3,
    "OPS_STATUS_CODE": "+"
}

response = requests.post(
    "http://localhost:8000/classify",
    json=[payload]
)

print(response.json())
# Output: [{"label": "PRATA"}]
```

---

### 🤝 **Contributing**

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📜 **License**

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) for details.

---

### 🏆 **Acknowledgments**

- **NASA Space Apps Challenge 2025** for the inspiration
- **UCS Satellite Database** for comprehensive satellite data
- **scikit-learn** community for excellent ML tools
- **FastAPI** & **React** teams for amazing frameworks

---

### 📧 **Contact**

**Project Link:** https://github.com/anibalssilva/OrbitHub

**Developed for NASA Space Apps Challenge 2025** 🚀

---

<div align="center">

**Made with ❤️ for a sustainable space future**

</div>

---
---
---

## Português

### 🌟 **Visão Geral**

**OrbitHub** é uma plataforma inovadora alimentada por ML que classifica satélites baseada em critérios de sustentabilidade e fornece um portal intuitivo bilíngue (EN/PT) para clientes solicitarem dados de satélites. Desenvolvido para o **NASA Space Apps Challenge 2025**, o OrbitHub aborda a necessidade crítica de avaliação de impacto ambiental em missões espaciais.

### 🎯 **Declaração do Problema**

Com mais de **5.000 satélites ativos** orbitando a Terra, entender sua pegada ambiental é crucial para:
- 🌱 Reduzir detritos espaciais
- ♻️ Promover missões espaciais sustentáveis
- 📊 Tomada de decisão informada para operadores de satélites
- 🔍 Relatórios de sustentabilidade transparentes

### 💡 **Solução**

OrbitHub introduz um **sistema de classificação de sustentabilidade de 3 níveis** (OURO 🥇 / PRATA 🥈 / BRONZE 🥉) usando **aprendizado de máquina não supervisionado (clustering KMeans)** baseado em:

| **Critério** | **Peso** | **Descrição** |
|--------------|---------|---------------|
| 🎯 **Alinhamento de Propósito** | 40% | Missões ambientais/observação da Terra pontuam mais alto |
| ⏰ **Tempo de Vida** | 30% | Vida operacional mais longa = melhor utilização de recursos |
| 🔧 **Capacidades** | 20% | Satélites multifuncionais são mais eficientes |
| 🌍 **Impacto Ambiental** | 10% | Parâmetros orbitais mais baixos = risco reduzido de detritos |

---

### 🏗️ **Arquitetura**

*(Mesma arquitetura ilustrada acima)*

---

### 🚀 **Funcionalidades**

#### **🔍 Classificação de Satélites**
- ✅ **Clustering KMeans** com 3 níveis de sustentabilidade
- ✅ **Engenharia de features automatizada** do UCS Satellite Database
- ✅ **Algoritmo de pontuação composta** (propósito + tempo + capacidades + impacto)
- ✅ **Cache habilitado** para respostas rápidas da API

#### **🌐 Portal Bilíngue (EN/PT)**
- ✅ **Troca de idioma dinâmica** (Inglês/Português)
- ✅ **40+ finalidades de satélite** (Observação da Terra, Comunicações, etc.)
- ✅ **195+ países** suportados no cadastro do cliente
- ✅ **Seleção múltipla de satélites** com interface de checkbox
- ✅ **Filtragem em tempo real** por classe de sustentabilidade & finalidade

#### **📋 Gerenciamento de Solicitações de Clientes**
- ✅ **Coleta de dados abrangentes do cliente** (nome, CNPJ, setor, país)
- ✅ **Opções de entrega flexíveis** (API / Batch)
- ✅ **Geração de relatórios bilíngues** (formato TXT)
- ✅ **Logging JSONL** para análise de requisições

#### **🎨 UI/UX Moderna**
- ✅ **Tema escuro futurista** com acentos neon
- ✅ **Design responsivo** (mobile/tablet/desktop)
- ✅ **Canvas espacial animado** como fundo
- ✅ **Sistema de ajuda baseado em tooltips** para todos os campos do formulário

---

### 📊 **Detalhes do Machine Learning**

*(Mesmos detalhes técnicos do ML descritos acima)*

---

### 🛠️ **Stack Tecnológica**

| Camada | Tecnologia | Propósito |
|--------|-----------|-----------|
| **Frontend** | React 18 + Vite 5 | SPA com hot-reload |
| **Backend** | FastAPI 0.110+ | API REST assíncrona |
| **ML** | scikit-learn 1.3+ | Clustering KMeans |
| **Dados** | pandas + openpyxl | Processamento de dados |
| **Servidor** | Uvicorn | Servidor ASGI |
| **Estilização** | CSS Customizado | UI Futurista |

---

### 📦 **Instalação & Configuração**

#### **Pré-requisitos**
- Python 3.11+
- Node.js 18+
- npm/yarn

#### **1. Clonar Repositório**
```bash
git clone https://github.com/anibalssilva/OrbitHub.git
cd OrbitHub
```

#### **2. Configuração do Backend**
```powershell
# Navegar para o diretório backend
cd backend

# Instalar dependências Python
pip install -r requirements.txt

# Treinar o modelo ML (apenas na primeira vez)
python -m app.train

# Gerar classificações iniciais
python -m app.predict

# Iniciar o servidor da API
python -m uvicorn app.main:app --port 8000 --reload
```

✅ **Backend rodando em:** `http://localhost:8000`  
📄 **Docs da API:** `http://localhost:8000/docs`

#### **3. Configuração do Frontend**
```powershell
# Navegar para o diretório frontend (da raiz do projeto)
cd frontend

# Instalar dependências Node
npm install

# Iniciar servidor de desenvolvimento
npm run dev -- --host --port 5173
```

✅ **Frontend rodando em:** `http://localhost:5173`

#### **4. Acessar a Aplicação**
- **Homepage:** http://localhost:5173/
- **Portal:** http://localhost:5173/portal.html
- **Docs da API:** http://localhost:8000/docs

---

### 📁 **Estrutura do Projeto**

*(Mesma estrutura de diretórios descrita acima)*

---

### 🌐 **Endpoints da API**

*(Mesmos endpoints descritos acima)*

---

### 🚀 **Deploy**

#### **Opção 1: Railway (Backend)**
1. Cadastre-se em https://railway.app
2. Conecte o repositório GitHub
3. Defina diretório raiz: `backend/`
4. Configure comando de build:
   ```bash
   pip install -r requirements.txt && python -m app.train && python -m app.predict
   ```
5. Defina comando de start:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

#### **Opção 2: Vercel (Frontend)**
1. Cadastre-se em https://vercel.com
2. Importe o repositório Git
3. Defina diretório raiz: `frontend/`
4. Framework preset: Vite
5. Adicione variável de ambiente:
   - `VITE_API_URL`: URL do seu backend Railway

Veja [DEPLOYMENT.md](./DEPLOYMENT.md) para instruções detalhadas.

---

### 📝 **Exemplo de Uso**

```python
# Exemplo: Classificar um novo satélite
import requests

payload = {
    "PURPOSE": "Communications",
    "LIFETIME_YEARS": 10.0,
    "CAPABILITIES_COUNT": 3,
    "OPS_STATUS_CODE": "+"
}

response = requests.post(
    "http://localhost:8000/classify",
    json=[payload]
)

print(response.json())
# Saída: [{"label": "PRATA"}]
```

---

### 🤝 **Contribuindo**

Contribuições são bem-vindas! Por favor:
1. Faça fork do repositório
2. Crie um branch de feature (`git checkout -b feature/RecursoIncrivel`)
3. Faça commit das mudanças (`git commit -m 'Adiciona RecursoIncrivel'`)
4. Faça push para o branch (`git push origin feature/RecursoIncrivel`)
5. Abra um Pull Request

---

### 📜 **Licença**

Este projeto está licenciado sob a **Licença MIT** - veja [LICENSE](./LICENSE) para detalhes.

---

### 🏆 **Agradecimentos**

- **NASA Space Apps Challenge 2025** pela inspiração
- **UCS Satellite Database** por dados abrangentes de satélites
- Comunidade **scikit-learn** por excelentes ferramentas de ML
- Times **FastAPI** & **React** por frameworks incríveis

---

### 📧 **Contato**

**Link do Projeto:** https://github.com/anibalssilva/OrbitHub

**Desenvolvido para NASA Space Apps Challenge 2025** 🚀

---

<div align="center">

**Feito com ❤️ para um futuro espacial sustentável**

</div>
