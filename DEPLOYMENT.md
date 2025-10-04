# 🚀 Guia de Deployment - OrbitHub

Este guia detalha como fazer o deploy da aplicação OrbitHub em produção.

---

## 📦 **Opções de Deploy**

### **Backend (FastAPI + Python)**
- ✅ Railway
- ✅ Render
- ✅ Heroku
- ✅ Google Cloud Run
- ✅ AWS Elastic Beanstalk

### **Frontend (React + Vite)**
- ✅ Vercel (Recomendado)
- ✅ Netlify
- ✅ GitHub Pages
- ✅ Cloudflare Pages

---

## 🎯 **Deploy do Backend**

### **Opção 1: Railway** (Recomendado)

1. **Crie uma conta** em [Railway.app](https://railway.app)

2. **Crie um novo projeto**:
   ```bash
   railway init
   ```

3. **Configure as variáveis de ambiente**:
   - Nenhuma variável obrigatória por padrão

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Configure o comando de start**:
   - Build Command: `pip install -r backend/requirements.txt && python -m app.train && python -m app.predict`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### **Opção 2: Render**

1. **Crie uma conta** em [Render.com](https://render.com)

2. **Crie um novo Web Service**

3. **Configurações**:
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     cd backend && python -m app.train && python -m app.predict
     ```
   - **Start Command**: 
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Root Directory**: `.`

4. **Deploy** automático via GitHub

### **Opção 3: Heroku**

1. **Instale o Heroku CLI**

2. **Login**:
   ```bash
   heroku login
   ```

3. **Crie um app**:
   ```bash
   heroku create orbithub-api
   ```

4. **Crie um `Procfile` na raiz**:
   ```
   web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Crie um `runtime.txt`**:
   ```
   python-3.11.0
   ```

6. **Deploy**:
   ```bash
   git push heroku main
   ```

---

## 🌐 **Deploy do Frontend**

### **Opção 1: Vercel** (Recomendado)

1. **Instale o Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

4. **Configurações** (vercel.json):
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "rewrites": [
       {
         "source": "/portal.html",
         "destination": "/portal.html"
       },
       {
         "source": "/(.*)",
         "destination": "/index.html"
       }
     ]
   }
   ```

5. **Configure a variável de ambiente**:
   - `VITE_API_URL`: URL do backend (ex: `https://orbithub-api.railway.app`)

### **Opção 2: Netlify**

1. **Crie uma conta** em [Netlify.com](https://netlify.com)

2. **Conecte o repositório GitHub**

3. **Configurações de Build**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. **Crie um `netlify.toml` na raiz**:
   ```toml
   [build]
     base = "frontend"
     command = "npm run build"
     publish = "dist"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

5. **Variáveis de Ambiente**:
   - `VITE_API_URL`: URL do backend

### **Opção 3: GitHub Pages**

1. **Instale o pacote gh-pages**:
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

2. **Adicione ao `package.json`**:
   ```json
   {
     "homepage": "https://anibalssilva.github.io/OrbitHub",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     }
   }
   ```

3. **Configure o `vite.config.js`**:
   ```javascript
   export default {
     base: '/OrbitHub/'
   }
   ```

4. **Deploy**:
   ```bash
   npm run deploy
   ```

---

## 🔗 **Conectando Frontend e Backend**

### **Atualizar URL da API no Frontend**

Edite `frontend/src/portal/App.jsx`:

```javascript
// Desenvolvimento
const API = 'http://localhost:8000'

// Produção
const API = import.meta.env.VITE_API_URL || 'https://sua-api.railway.app'
```

### **Configurar CORS no Backend**

O backend já está configurado para aceitar todas as origens. Para produção, recomenda-se restringir:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.vercel.app"],  # Especifique sua URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 **Monitoramento**

### **Backend**
- Health check endpoint: `https://sua-api.com/health`
- API Docs: `https://sua-api.com/docs`

### **Frontend**
- Verifique o console do navegador para erros
- Use o Network tab para verificar chamadas à API

---

## 🐛 **Troubleshooting**

### **Erro: ModuleNotFoundError: No module named 'app'**
- **Solução**: Certifique-se de que o comando de start está rodando a partir da pasta `backend`

### **Erro: CORS policy**
- **Solução**: Verifique se o backend permite a origem do frontend no `CORSMiddleware`

### **Erro: 404 Not Found**
- **Solução no Vercel/Netlify**: Configure os rewrites/redirects para SPAs

### **Erro: Module not found during build**
- **Solução**: Certifique-se de que todas as dependências estão no `package.json` e `requirements.txt`

---

## ✅ **Checklist de Deploy**

### **Backend**
- [ ] Todos os requirements instalados
- [ ] Modelo ML treinado
- [ ] Dados classificados
- [ ] CORS configurado corretamente
- [ ] Health check funcionando
- [ ] Porta configurada via variável de ambiente

### **Frontend**
- [ ] URL da API configurada
- [ ] Build funcionando sem erros
- [ ] Rewrites/redirects configurados
- [ ] Assets carregando corretamente
- [ ] Bilinguismo funcionando

---

## 🎉 **Deploy Completo!**

Após seguir estes passos, sua aplicação OrbitHub estará no ar!

**URLs de exemplo**:
- Frontend: `https://orbithub.vercel.app`
- Backend: `https://orbithub-api.railway.app`
- API Docs: `https://orbithub-api.railway.app/docs`

---

## 📞 **Suporte**

Se encontrar problemas, abra uma [issue no GitHub](https://github.com/anibalssilva/OrbitHub/issues).

