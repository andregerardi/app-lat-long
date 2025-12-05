# 🚀 GUIA RÁPIDO - Capturador GPS

## ⚡ Comece Agora em 3 Passos!

### Passo 1: Instale Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Execute o App
```bash
python app_flask.py
```

### Passo 3: Abra no Navegador
```
http://localhost:5000
```

---

## 📱 Para Testar em Android Físico

### No Windows PowerShell:
```powershell
.\run_test.ps1
```

Vai aparecer algo como:
```
IPv4 Address: 192.168.1.100
```

### No Android, acesse:
```
http://192.168.1.100:5000
```

---

## 🎯 O que Fazer Depois

1. **Clique em "📍 CAPTURAR LOCALIZAÇÃO"**
2. **Permita acesso ao GPS** quando pedir
3. **Visualize no mapa**
4. **Clique em "💾 Salvar Localização"**
5. **Vá à aba "📊 Histórico"** para ver todos os pontos

---

## 🌐 Deploy Online (5 minutos)

### Render.com (Gratuito)

1. Vá para https://render.com
2. Clique em "New +" → "Web Service"
3. Conecte seu GitHub
4. Selecione o repositório
5. Configure:
   - **Name:** gps-tracker
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app_flask:app`
6. Clique em "Deploy"
7. Aguarde (2-3 min) e use o link gerado!

---

## 📊 Dados Capturados

- ✅ Latitude & Longitude
- ✅ Altitude
- ✅ Velocidade
- ✅ Precisão GPS
- ✅ Data/Hora
- ✅ Nome do usuário
- ✅ Descrição

---

## 🔧 Troubleshooting

| Problema | Solução |
|----------|---------|
| Port 5000 já em uso | `python app_flask.py --port 5001` |
| Erro ao importar Flask | `pip install flask` |
| Não consegue capturar GPS | Ative GPS no Android e use HTTPS |
| "Conexão recusada" | Verifique firewall ou use IP correto |

---

## 💡 Dicas

- 🌍 Teste ao ar livre para melhor precisão
- 🔋 GPS consome bateria - teste com carregador plugado
- 📡 Espere 10-15 segundos para GPS conectar
- 🗺️ Veja todas as localizações no histórico
- 📲 Funciona em qualquer navegador moderno

---

**Desenvolvido com ❤️ para capturar localizações GPS**
