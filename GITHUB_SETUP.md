# 🐙 Guia Completo - Push para GitHub

Este guia te ajudará a fazer o push completo da aplicação OrbitHub para o GitHub.

---

## 📋 **Pré-requisitos**

1. **Git instalado**: Verifique com `git --version`
2. **Conta no GitHub**: [github.com](https://github.com)
3. **Repositório criado**: https://github.com/anibalssilva/OrbitHub.git

---

## 🚀 **Passo a Passo**

### **1. Inicialize o Git (se necessário)**

```powershell
# No diretório C:\NASA
git init
```

### **2. Configure o Git (primeira vez)**

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

### **3. Adicione o Remote**

```powershell
git remote add origin https://github.com/anibalssilva/OrbitHub.git
```

### **4. Verifique os arquivos**

```powershell
git status
```

### **5. Adicione todos os arquivos**

```powershell
git add .
```

### **6. Faça o commit**

```powershell
git commit -m "🚀 Initial commit - OrbitHub NASA Hackathon 2025

✨ Features:
- Machine Learning satellite classification (KMeans)
- Bilingual portal (EN/PT)
- Sustainability scoring (GOLD/SILVER/BRONZE)
- Multi-satellite selection
- Detailed TXT reports
- Futuristic UI/UX with neon effects
- FastAPI backend
- React + Vite frontend
- 40+ satellite purposes
- 195+ countries support"
```

### **7. Push para o GitHub**

```powershell
# Primeira vez
git branch -M main
git push -u origin main

# Próximas vezes
git push
```

---

## 🔐 **Autenticação no GitHub**

### **Opção 1: Personal Access Token (Recomendado)**

1. Vá em **GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)**
2. Clique em **"Generate new token (classic)"**
3. Selecione os escopos: `repo`, `workflow`
4. Copie o token
5. Ao fazer `git push`, use:
   - Username: `anibalssilva`
   - Password: `seu_token_copiado`

### **Opção 2: SSH Key**

1. Gere uma chave SSH:
   ```powershell
   ssh-keygen -t ed25519 -C "seu.email@example.com"
   ```

2. Adicione ao ssh-agent:
   ```powershell
   ssh-add ~\.ssh\id_ed25519
   ```

3. Copie a chave pública:
   ```powershell
   cat ~\.ssh\id_ed25519.pub
   ```

4. Adicione no GitHub:
   - **Settings > SSH and GPG keys > New SSH key**
   - Cole a chave pública

5. Configure o remote com SSH:
   ```powershell
   git remote set-url origin git@github.com:anibalssilva/OrbitHub.git
   ```

---

## 📦 **Estrutura de Commits Recomendada**

### **Padrão de Mensagens**

```
tipo(escopo): descrição curta

Descrição detalhada (opcional)

Footers (opcional)
```

### **Tipos de Commit**

- ✨ `feat`: Nova feature
- 🐛 `fix`: Correção de bug
- 📝 `docs`: Documentação
- 💄 `style`: Formatação, estilo
- ♻️ `refactor`: Refatoração de código
- ⚡ `perf`: Melhoria de performance
- ✅ `test`: Testes
- 🔧 `chore`: Manutenção, configs

### **Exemplos**

```powershell
git commit -m "✨ feat(ml): add KMeans satellite classification"
git commit -m "🐛 fix(api): resolve CORS issue"
git commit -m "📝 docs: update README with deployment guide"
```

---

## 🌿 **Trabalhando com Branches**

### **Criar uma nova branch**

```powershell
git checkout -b feature/nome-da-feature
```

### **Listar branches**

```powershell
git branch
```

### **Trocar de branch**

```powershell
git checkout main
```

### **Merge de branch**

```powershell
git checkout main
git merge feature/nome-da-feature
```

### **Deletar branch**

```powershell
git branch -d feature/nome-da-feature
```

---

## 🔄 **Atualizando o Repositório**

### **Pull (trazer mudanças)**

```powershell
git pull origin main
```

### **Push (enviar mudanças)**

```powershell
git push origin main
```

### **Status do repositório**

```powershell
git status
git log --oneline
```

---

## 🏷️ **Tags e Releases**

### **Criar uma tag**

```powershell
git tag -a v1.0.0 -m "Release version 1.0.0 - NASA Hackathon 2025"
```

### **Push da tag**

```powershell
git push origin v1.0.0
```

### **Listar tags**

```powershell
git tag
```

---

## 🎯 **GitHub Actions (CI/CD)**

Crie `.github/workflows/main.yml`:

```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Train model
        run: |
          cd backend
          python -m app.train
      - name: Classify satellites
        run: |
          cd backend
          python -m app.predict

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Build
        run: |
          cd frontend
          npm run build
```

---

## 📊 **GitHub Project Boards**

1. Vá em **Projects** no seu repositório
2. Crie um **New project**
3. Escolha template **Kanban** ou **Table**
4. Organize suas tasks:
   - 📋 **To Do**
   - 🔄 **In Progress**
   - ✅ **Done**

---

## 🔒 **Secrets do GitHub**

Para deploy automático, configure secrets:

1. **Settings > Secrets and variables > Actions**
2. **New repository secret**
3. Adicione:
   - `VERCEL_TOKEN`
   - `RAILWAY_TOKEN`
   - etc.

---

## 🐛 **Troubleshooting**

### **Erro: remote origin already exists**
```powershell
git remote remove origin
git remote add origin https://github.com/anibalssilva/OrbitHub.git
```

### **Erro: failed to push some refs**
```powershell
git pull origin main --rebase
git push origin main
```

### **Erro: Authentication failed**
- Use um Personal Access Token
- Ou configure SSH keys

### **Arquivo muito grande (>100MB)**
```powershell
# Adicione ao .gitignore
echo "arquivo_grande.xlsx" >> .gitignore
git rm --cached arquivo_grande.xlsx
git commit -m "Remove large file"
```

---

## ✅ **Checklist Final**

Antes de fazer o push:

- [ ] `.gitignore` configurado corretamente
- [ ] README.md completo e atualizado
- [ ] LICENSE adicionado
- [ ] Dados sensíveis removidos
- [ ] Secrets não commitados
- [ ] Build do frontend funcionando
- [ ] Modelo ML treinado (ou excluído do commit se muito grande)
- [ ] Documentação clara
- [ ] Testes passando (se houver)

---

## 🎉 **Pronto!**

Agora seu projeto OrbitHub está no GitHub e pronto para:
- ⭐ Receber stars
- 🍴 Ser forked
- 🤝 Receber contribuições
- 🚀 Ser deployado

---

## 📞 **Comandos Rápidos**

```powershell
# Ver status
git status

# Adicionar tudo
git add .

# Commit
git commit -m "mensagem"

# Push
git push

# Pull
git pull

# Ver diferenças
git diff

# Ver log
git log --oneline --graph

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer mudanças em arquivo
git checkout -- arquivo.txt

# Ver remote
git remote -v
```

---

**🌟 Boa sorte no NASA Space Apps Challenge 2025! 🚀**

