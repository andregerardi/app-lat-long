#!/bin/bash
# Script para testar a aplicação

echo "📍 Capturador GPS - Script de Teste"
echo "===================================="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo "1️⃣ Verificando Python..."
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python encontrado$(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python não encontrado${NC}"
    exit 1
fi

# Instalar dependências
echo ""
echo "2️⃣ Instalando dependências..."
pip install -r requirements.txt

# Verificar Flask
echo ""
echo "3️⃣ Testando Flask..."
python3 -c "import flask; print(f'✓ Flask {flask.__version__}')" 2>/dev/null || {
    echo -e "${RED}✗ Erro ao importar Flask${NC}"
    exit 1
}

# Verificar SQLite
echo ""
echo "4️⃣ Testando SQLite..."
python3 -c "import sqlite3; print('✓ SQLite OK')" || {
    echo -e "${RED}✗ Erro ao importar SQLite${NC}"
    exit 1
}

# Iniciando servidor
echo ""
echo -e "${YELLOW}5️⃣ Iniciando servidor Flask...${NC}"
echo ""
echo "📍 Acesse em http://localhost:5000"
echo "📱 Para Android na mesma rede: http://SEU_IP_PC:5000"
echo ""
echo "Para descobrir seu IP:"
echo "  Windows: ipconfig (procure por IPv4 Address)"
echo "  Linux/Mac: ifconfig ou ip addr"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""

python3 app_flask.py
