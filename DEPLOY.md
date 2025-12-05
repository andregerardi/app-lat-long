# 🚀 Guia de Deploy Flask - Capturador GPS

## ⚡ Deploy Rápido (5 minutos)

### Opção 1: Render.com ⭐ (RECOMENDADO - Gratuito)

**Vantagens:**
- ✅ Gratuito
- ✅ Automático (conecta com GitHub)
- ✅ HTTPS incluído
- ✅ Suporta Python/Flask perfeitamente

**Passos:**

1. **Vá para https://render.com**
2. **Clique em "New +"** → **"Web Service"**
3. **Conecte seu GitHub** e selecione o repositório `app-lat-long`
4. **Configure assim:**
   - Name: `gps-tracker` (ou qualquer nome)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_flask:app`
   - Instance Type: Free

5. **Clique em "Deploy"**
6. **Aguarde 2-3 minutos** ☕
7. **Seu app estará em:** `https://gps-tracker.onrender.com`

**Pronto! Deploy automático a cada push no GitHub!** 🎉

---

### Opção 2: Heroku (Precisa de Cartão)

**Passos:**

1. **Instale Heroku CLI:**
   ```bash
   # Windows: baixe em https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Faça login:**
   ```bash
   heroku login
   ```

3. **Crie o app:**
   ```bash
   heroku create seu-gps-app
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Veja os logs:**
   ```bash
   heroku logs --tail
   ```

**URL:** `https://seu-gps-app.herokuapp.com`

---

### Opção 3: PythonAnywhere (Fácil)

1. Vá para https://www.pythonanywhere.com
2. Crie conta gratuita
3. Upload dos arquivos via File interface
4. Configure WSGI

---

## 🔑 Arquivos Necessários para Deploy

Já criamos tudo! Você tem:

```
✅ app_flask.py           - Aplicação
✅ templates/index.html   - Interface
✅ requirements.txt       - Dependências
✅ Procfile               - Instruções de deploy
✅ .gitignore             - Arquivos a ignorar
```

---

## 🎯 Passo-a-Passo Completo (Render)

### 1. Prepare o repositório
```bash
cd "c:\Users\dirceu.gerardi\Desktop\2025-superacao\Georeferenciamento"
git add -A
git commit -m "Ready for deployment"
git push origin main
```

### 2. Crie uma conta Render
- Acesse: https://render.com
- Clique em "Sign up"
- Use sua conta GitHub

### 3. Crie um novo serviço
- Clique em "New +"
- Selecione "Web Service"
- Autorize acesso ao GitHub
- Selecione `app-lat-long`

### 4. Configure
```
Name:                 gps-tracker
Environment:          Python 3
Region:               São Paulo (syd) se disponível
Branch:               main
Build Command:        pip install -r requirements.txt
Start Command:        gunicorn app_flask:app
Instance Type:        Free
```

### 5. Deploy
- Clique em "Deploy"
- Aguarde a compilação
- Seu URL aparecerá em ~3 minutos

---

## 📱 Testar Online

### No PC:
```
https://gps-tracker.onrender.com
```

### No Android:
```
# Mesma URL acima funciona de qualquer lugar!
https://gps-tracker.onrender.com
```

---

## 🔍 Verificar Logs

### Render:
```
Dashboard → Seu App → Logs
```

### Heroku:
```bash
heroku logs --tail
```

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| "Build failed" | Verifique se `requirements.txt` está correto |
| "502 Bad Gateway" | Veja os logs - pode ser erro no app |
| "Module not found" | Certifique-se que está em `requirements.txt` |
| Banco de dados vazio | Dados são salvos no servidor (SQLite) |

---

## 💡 Dicas Importantes

1. **Banco de dados local**: O SQLite salva tudo no servidor, não no seu PC
2. **Arquivos**: Se precisar salvar arquivos, use plataformas com storage (AWS S3, etc)
3. **Variáveis de ambiente**: Para dados sensíveis, use env vars
4. **Cold start**: Render dorme apps gratuitos, primeira requisição é lenta

---

## 🌍 URLs Finais

- **Render:** `https://gps-tracker.onrender.com`
- **Heroku:** `https://seu-gps-app.herokuapp.com`
- **Local:** `http://localhost:5000`

---

**Pronto! Seu app estará online em poucos minutos!** 🚀
