#!/bin/bash
# Script rápido para fazer deploy

echo "📍 Capturador GPS - Deploy Rápido"
echo "=================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1️⃣ Atualizando código no GitHub...${NC}"
git add -A
git commit -m "Deploy update"
git push origin main

echo ""
echo -e "${GREEN}✅ Código atualizado!${NC}"
echo ""
echo "📝 Próximos passos:"
echo "   1. Vá para https://render.com"
echo "   2. Sign Up com GitHub"
echo "   3. New → Web Service"
echo "   4. Selecione: andregerardi/app-lat-long"
echo "   5. Preencha conforme DEPLOY_PASSO_A_PASSO.md"
echo "   6. Clique Deploy"
echo ""
echo "⏱️  Seu app estará online em 2-3 minutos!"
echo ""
