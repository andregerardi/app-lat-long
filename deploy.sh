#!/bin/bash
# Script para facilitar o deploy no Streamlit Cloud

echo "📍 Capturador GPS - Script de Deploy"
echo "===================================="
echo ""

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Instale em: https://git-scm.com"
    exit 1
fi

echo "1️⃣ Inicializando repositório Git..."
git init

echo "2️⃣ Adicionando arquivos..."
git add app_streamlit.py requirements.txt README.md .streamlit/config.toml .gitignore

echo "3️⃣ Criando commit inicial..."
git commit -m "Initial commit - GPS Location Tracker with Streamlit"

echo ""
echo "4️⃣ Próximos passos:"
echo "   ├─ Crie um repositório no GitHub: https://github.com/new"
echo "   ├─ Copie o comando 'git remote add origin' do GitHub"
echo "   ├─ Execute: git branch -M main"
echo "   ├─ Execute: git push -u origin main"
echo "   └─ Acesse: https://streamlit.io/cloud e faça deploy"
echo ""
echo "✅ Repositório local pronto para deploy!"
