# 🚀 Como Iniciar os Servidores

## ⚠️ IMPORTANTE: Ordem de Comandos

### 1️⃣ Iniciar o Backend (FastAPI)

Abra um terminal PowerShell e execute:

```powershell
# Vá para a pasta backend
cd backend

# Inicie o servidor
python -m uvicorn app.main:app --port 8000 --reload
```

O servidor deve iniciar em: `http://localhost:8000`

### 2️⃣ Iniciar o Frontend (Vite + React)

Abra OUTRO terminal PowerShell e execute:

```powershell
# Vá para a pasta frontend
cd frontend

# Inicie o servidor
npm run dev -- --host --port 5173
```

O servidor deve iniciar em: `http://localhost:5174` (ou 5173)

## 🧪 Testar se o Backend está funcionando

Depois de iniciar o backend, teste no navegador:

- Health check: `http://localhost:8000/health`
- Satélites: `http://localhost:8000/satellites?limit=3`

## 📋 Estrutura Esperada

```
C:\NASA\
├── backend\
│   ├── app\
│   │   ├── main.py
│   │   ├── data_access.py
│   │   ├── features.py
│   │   └── models\
│   ├── data\
│   │   ├── raw\
│   │   │   └── UCS-Satellite-Database 5-1-2023.xlsx
│   │   └── processed\
│   │       └── satellites_classified.csv
│   └── requirements.txt
└── frontend\
    ├── index.html
    ├── portal.html
    └── src\
        └── portal\
            ├── App.jsx
            └── style.css
```

## ❌ Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'app'"

**Solução**: Certifique-se de estar na pasta `backend` ao executar o comando `python -m uvicorn app.main:app --port 8000 --reload`

### Erro: "Cannot find module 'app'"

**Solução**: Você está no diretório errado. Use `cd backend` primeiro.

### Porta em uso

**Solução**: Mate todos os processos Python:
```powershell
Get-Process | Where-Object {$_.Name -like "*python*"} | Stop-Process -Force
```

