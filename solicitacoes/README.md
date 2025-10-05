# 📋 Solicitações de Dados de Satélites

Esta pasta contém os relatórios legíveis das solicitações de dados de satélites enviadas através do portal OrbitHub.

## 📁 Estrutura dos Arquivos

Os arquivos são nomeados no formato:
```
solicitacao_{nome_cliente}_{timestamp}.txt
```

Exemplo:
```
solicitacao_Joao_Silva_20250105_143022.txt
```

## 📋 Conteúdo dos Relatórios

Cada arquivo contém:
- ✅ Informações do cliente (nome, CNPJ, endereço, email, setor, país)
- ✅ Detalhes da solicitação (finalidade, classificação, tipo de entrega, descrição)
- ✅ Lista de satélites selecionados com detalhes completos
- ✅ Timestamp da solicitação
- ✅ Formato bilíngue (português/inglês)

## 🔄 Geração Automática

Os arquivos são criados automaticamente quando:
1. Um cliente preenche o formulário no portal
2. Seleciona satélites de interesse
3. Envia a solicitação

## 📊 Log de Processamento

Para processamento automatizado, consulte:
- `../data/processed/portal_requests.jsonl` - Log JSON das requisições

---
**OrbitHub - NASA Space Apps Challenge 2025** 🚀
