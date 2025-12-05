@echo off
REM Script para facilitar deploy no Render

echo.
echo 📍 Capturador GPS - Deploy Helper
echo ==================================
echo.

REM Verificar se está em um repositório git
if not exist ".git" (
    echo ❌ Erro: não está em um repositório Git
    echo Inicialize com: git init
    pause
    exit /b 1
)

REM Verificar se há mudanças
echo 1️⃣ Verificando mudanças...
git status
echo.

REM Perguntar se quer fazer commit
set /p COMMIT="Fazer commit das mudanças? (s/n): "
if /i "%COMMIT%"=="s" (
    set /p MSG="Digite a mensagem do commit: "
    git add -A
    git commit -m "%MSG%"
    echo ✓ Commit realizado
) else (
    echo ⊘ Commit cancelado
)

echo.
echo 2️⃣ Enviando para GitHub...
git push origin main
if errorlevel 1 (
    echo ❌ Erro ao fazer push
    pause
    exit /b 1
)

echo.
echo ✅ Deploy pronto!
echo.
echo 📝 Próximos passos:
echo   1. Acesse https://render.com
echo   2. Clique em "New +" → "Web Service"
echo   3. Conecte seu GitHub e selecione app-lat-long
echo   4. Configure conforme o guia DEPLOY.md
echo   5. Clique em "Deploy"
echo.
echo Seu app estará online em ~3 minutos!
echo.
pause
