# 📍 Capturador GPS com Streamlit

Sistema online para capturar localização GPS de dispositivos Android em tempo real.

## 🚀 Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone ou baixe o projeto:**
```bash
cd Georeferenciamento
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o aplicativo:**
```bash
streamlit run app_streamlit.py
```

4. **Acesse no navegador:**
```
http://localhost:8501
```

## 🌐 Deploy Online (Gratuito)

### Opção 1: Streamlit Cloud ⭐ (Recomendado)

**Vantagens:**
- Hospedagem gratuita
- Deploy automático via GitHub
- Ideal para aplicações Streamlit

**Passos:**

1. **Crie um repositório GitHub:**
   - Vá para https://github.com/new
   - Crie um repositório chamado `georeferenciamento-gps`
   - Clone localmente

2. **Adicione seus arquivos:**
```bash
git add app_streamlit.py requirements.txt README.md
git commit -m "Initial commit"
git push origin main
```

3. **Faça deploy no Streamlit Cloud:**
   - Vá para https://streamlit.io/cloud
   - Clique em "New app"
   - Selecione seu repositório GitHub
   - Configure:
     - Repository: seu-usuario/georeferenciamento-gps
     - Branch: main
     - Main file path: app_streamlit.py
   - Clique em "Deploy"

4. **Compartilhe o link:**
   - Seu app estará disponível em: `https://seu-usuario-georeferenciamento-gps.streamlit.app`

### Opção 2: PythonAnywhere (Gratuito)

1. Crie conta em https://www.pythonanywhere.com
2. Upload o código via Web interface
3. Configure a aplicação WSGI
4. Seu URL: `https://seu-usuario.pythonanywhere.com`

### Opção 3: Render (Gratuito)

1. Vá para https://render.com
2. Crie novo "Web Service"
3. Conecte seu repositório GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app_streamlit.py --server.port=10000`

## 📱 Como Usar no Android

1. **Abra um navegador** (Chrome, Firefox, etc)
2. **Acesse a URL** do aplicativo online
3. **Permita acesso ao GPS** quando solicitado
4. **Clique em "📍 CAPTURAR LOCALIZAÇÃO"**
5. **Visualize o mapa** e salve os dados

## 🎯 Recursos

- ✅ Captura de GPS em tempo real
- ✅ Mapa interativo com folium
- ✅ Banco de dados SQLite integrado
- ✅ Histórico completo de localizações
- ✅ Exportação em CSV e JSON
- ✅ Suporte a múltiplos usuários
- ✅ Precisão e altitude
- ✅ Interface responsiva

## 📊 Estrutura de Dados

### Tabela: locations
```
id: Identificador único
latitude: Coordenada de latitude
longitude: Coordenada de longitude
altitude: Altitude em metros
speed: Velocidade em m/s
accuracy: Precisão em metros
timestamp: Data/hora da captura
user_name: Nome do usuário
description: Descrição/observações
```

## 🔒 Segurança

- Os dados são armazenados localmente (no servidor)
- Acesso via HTTPS é recomendado
- Nenhuma informação sensível é transmitida
- Geolocalização requer permissão explícita do usuário

## 🛠️ Configurações Avançadas

### Alterar Puerto Local
```bash
streamlit run app_streamlit.py --server.port=8000
```

### Desabilitar Upload de Arquivo
```bash
streamlit run app_streamlit.py --client.showErrorDetails=false
```

## ⚠️ Limitações e Notas

- GPS funciona melhor ao ar livre
- Precisão depende do dispositivo e condições
- Alguns navegadores/dispositivos podem ter restrições
- A bateria do dispositivo será consumida mais rapidamente

## 📞 Suporte

Para problemas ou sugestões, verifique:
- https://streamlit.io/docs
- https://github.com/streamlit/streamlit/issues
- https://folium.readthedocs.io/

## 📄 Licença

MIT - Livre para uso e modificação

---

**Desenvolvido com ❤️ usando Streamlit e Python**
# app-lat-long
