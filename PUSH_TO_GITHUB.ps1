# Script PowerShell para fazer push do OrbitHub para o GitHub
# Execute este script no PowerShell com: .\PUSH_TO_GITHUB.ps1

Write-Host "🚀 OrbitHub - Push para GitHub" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar se Git está instalado
Write-Host "📝 Verificando instalação do Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não está instalado! Instale em: https://git-scm.com" -ForegroundColor Red
    exit 1
}

# 2. Verificar se estamos no diretório correto
$currentDir = Get-Location
Write-Host "📁 Diretório atual: $currentDir" -ForegroundColor Yellow

# 3. Verificar se .git existe
if (Test-Path ".git") {
    Write-Host "✅ Repositório Git já inicializado" -ForegroundColor Green
} else {
    Write-Host "📦 Inicializando repositório Git..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repositório Git inicializado" -ForegroundColor Green
}

# 4. Configurar remote
Write-Host "🔗 Configurando remote origin..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "⚠️  Remote origin já existe. Removendo..." -ForegroundColor Yellow
    git remote remove origin
}
git remote add origin https://github.com/anibalssilva/OrbitHub.git
Write-Host "✅ Remote configurado: https://github.com/anibalssilva/OrbitHub.git" -ForegroundColor Green

# 5. Verificar branch
Write-Host "🌿 Verificando branch..." -ForegroundColor Yellow
$currentBranch = git branch --show-current
if ($currentBranch -eq "") {
    Write-Host "📝 Nenhuma branch detectada. Criando branch 'main'..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "✅ Branch 'main' criada" -ForegroundColor Green
} else {
    Write-Host "✅ Branch atual: $currentBranch" -ForegroundColor Green
    if ($currentBranch -ne "main") {
        Write-Host "🔄 Renomeando para 'main'..." -ForegroundColor Yellow
        git branch -M main
    }
}

# 6. Verificar status
Write-Host ""
Write-Host "📊 Status do repositório:" -ForegroundColor Yellow
git status --short

# 7. Adicionar arquivos
Write-Host ""
Write-Host "➕ Adicionando arquivos ao commit..." -ForegroundColor Yellow
git add .
Write-Host "✅ Arquivos adicionados" -ForegroundColor Green

# 8. Commit
Write-Host ""
Write-Host "💾 Criando commit..." -ForegroundColor Yellow
$commitMessage = @"
🚀 Initial commit - OrbitHub NASA Hackathon 2025

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
- 195+ countries support

📦 Stack:
- Backend: Python 3.11, FastAPI, scikit-learn, pandas
- Frontend: React 18, Vite, CSS3
- ML: KMeans clustering for sustainability classification
- Data: UCS Satellite Database 5-1-2023

🌍 NASA Space Apps Challenge 2025
"@

git commit -m $commitMessage
Write-Host "✅ Commit criado" -ForegroundColor Green

# 9. Push
Write-Host ""
Write-Host "🚀 Fazendo push para o GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Você precisará fazer login no GitHub!" -ForegroundColor Cyan
Write-Host ""

try {
    git push -u origin main
    Write-Host ""
    Write-Host "✅ ✅ ✅ PUSH REALIZADO COM SUCESSO! ✅ ✅ ✅" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Seu projeto OrbitHub está agora no GitHub!" -ForegroundColor Cyan
    Write-Host "🔗 Acesse: https://github.com/anibalssilva/OrbitHub" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Próximos passos:" -ForegroundColor Yellow
    Write-Host "  1. Acesse o repositório no GitHub" -ForegroundColor White
    Write-Host "  2. Adicione uma descrição ao repositório" -ForegroundColor White
    Write-Host "  3. Adicione topics: nasa, hackathon, satellite, ml, fastapi, react" -ForegroundColor White
    Write-Host "  4. Configure GitHub Pages (se desejar)" -ForegroundColor White
    Write-Host "  5. Considere fazer deploy (veja DEPLOYMENT.md)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push!" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔐 Opções de autenticação:" -ForegroundColor Yellow
    Write-Host "  1. Use um Personal Access Token (recomendado)" -ForegroundColor White
    Write-Host "     - Vá em GitHub > Settings > Developer settings > Personal access tokens" -ForegroundColor White
    Write-Host "     - Crie um novo token com permissão 'repo'" -ForegroundColor White
    Write-Host "     - Use o token como senha ao fazer push" -ForegroundColor White
    Write-Host ""
    Write-Host "  2. Configure SSH keys" -ForegroundColor White
    Write-Host "     - Execute: ssh-keygen -t ed25519 -C 'seu.email@example.com'" -ForegroundColor White
    Write-Host "     - Adicione a chave pública no GitHub" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Mais detalhes em: GITHUB_SETUP.md" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🌟 Boa sorte no NASA Space Apps Challenge 2025! 🚀" -ForegroundColor Cyan

