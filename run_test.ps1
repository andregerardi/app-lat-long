Write-Host "📍 Capturador GPS - Script de Teste" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1️⃣ Verificando Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    python --version
    Write-Host "✓ Python encontrado" -ForegroundColor Green
} else {
    Write-Host "✗ Python não encontrado" -ForegroundColor Red
    Write-Host "Instale Python de https://www.python.org" -ForegroundColor Red
    exit 1
}

# Instalar dependências
Write-Host ""
Write-Host "2️⃣ Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Testando imports
Write-Host ""
Write-Host "3️⃣ Testando imports..." -ForegroundColor Yellow
python -c "import flask; print('✓ Flask OK')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Erro ao importar Flask" -ForegroundColor Red
    exit 1
}

python -c "import sqlite3; print('✓ SQLite OK')" 2>$null

# Iniciando servidor
Write-Host ""
Write-Host "5️⃣ Iniciando servidor Flask..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Acesse em http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Para Android na mesma rede:" -ForegroundColor Green
Write-Host "   1. Execute: ipconfig" -ForegroundColor White
Write-Host "   2. Procure por 'IPv4 Address' (ex: 192.168.1.100)" -ForegroundColor White
Write-Host "   3. Acesse http://192.168.1.100:5000" -ForegroundColor White
Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

python app_flask.py
