# 📍 Capturador GPS com Flask

Sistema online para capturar localização GPS de dispositivos Android em tempo real.

## ⚡ Versões Disponíveis

### 🔴 Streamlit (app_streamlit.py) - COM PROBLEMAS
- Dificuldade em passar dados do JavaScript para Python
- Não recomendado para captura de GPS em produção

### 🟢 Flask (app_flask.py) - **RECOMENDADO** ⭐
- ✅ Captura GPS funcional 100%
- ✅ Interface HTML/CSS moderna
- ✅ API REST completa
- ✅ Funciona em Android físico
- ✅ Mapa interativo com Leaflet

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Execute o Flask app (RECOMENDADO):**
```bash
python app_flask.py
```

3. **Acesse no navegador:**
```
http://localhost:5000
```

### Para Acessar do Android

Se estiver testando de um celular Android na mesma rede:

1. **Descubra o IP do seu PC:**
   ```bash
   ipconfig
   ```
   Procure por "IPv4 Address" (ex: 192.168.1.100)

2. **Acesse do Android:**
   ```
   http://192.168.1.100:5000
   ```

## 🌐 Deploy Online

### Opção 1: Render (Gratuito) ⭐

1. Crie conta em https://render.com
2. Crie novo "Web Service"
3. Conecte seu repositório GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app_flask:app`
6. Aguarde o deploy

### Opção 2: Heroku (Precisa Adicionar Procfile)

1. Crie um arquivo `Procfile`:
```
web: gunicorn app_flask:app
```

2. Instale Heroku CLI e faça deploy:
```bash
heroku create seu-app-gps
git push heroku main
```

### Opção 3: PythonAnywhere

1. Vá para https://www.pythonanywhere.com
2. Upload dos arquivos
3. Configure WSGI

## 📱 Como Usar

### Local (PC)

1. Execute: `python app_flask.py`
2. Abra http://localhost:5000
3. Clique em "📍 CAPTURAR LOCALIZAÇÃO"
4. Permita acesso ao GPS (seu PC precisa ter GPS ou simulate)

### Android Físico

1. Conecte à mesma rede do PC ou acesse online
2. **Ative o GPS** no celular
3. Abra o navegador e acesse a URL
4. Clique em "📍 CAPTURAR LOCALIZAÇÃO"
5. Permita acesso ao GPS quando solicitado
6. Visualize no mapa e salve os dados

## 🎯 Recursos

- ✅ Captura de GPS em tempo real
- ✅ Mapa interativo com Leaflet
- ✅ Banco de dados SQLite integrado
- ✅ Histórico completo de localizações
- ✅ Suporte a múltiplos usuários
- ✅ Precisão, altitude e velocidade
- ✅ Interface responsiva (funciona em celular)
- ✅ API REST para integração

## 📊 API REST

### Endpoints Disponíveis

#### 1. Salvar Localização
```
POST /api/save-location
Content-Type: application/json

{
    "latitude": -23.550520,
    "longitude": -46.633309,
    "altitude": 750,
    "speed": 0,
    "accuracy": 10,
    "user_name": "João",
    "description": "Pico da Consolação"
}
```

#### 2. Obter Histórico
```
GET /api/get-locations

Response:
[
    {
        "id": 1,
        "latitude": -23.550520,
        "longitude": -46.633309,
        "altitude": 750,
        "speed": 0,
        "accuracy": 10,
        "timestamp": "2025-12-05T10:30:00.000000",
        "user_name": "João",
        "description": "Pico da Consolação"
    }
]
```

#### 3. Deletar Localização
```
DELETE /api/delete-location/1
```

## 📂 Estrutura de Arquivos

```
Georeferenciamento/
├── app_flask.py              # ⭐ App principal (USAR ESTE)
├── app_streamlit.py          # App Streamlit (alternativa)
├── requirements.txt          # Dependências
├── locations.db              # Banco de dados (criado automaticamente)
├── templates/
│   └── index.html            # Interface HTML
├── README.md                 # Este arquivo
└── .gitignore
```

## 🔒 Segurança

- Dados salvos localmente (no servidor)
- Use HTTPS em produção (Render, Heroku fazem automaticamente)
- Geolocalização requer permissão explícita do usuário

## ⚠️ Notas Importantes

- **GPS funciona melhor ao ar livre**
- Alguns navegadores/dispositivos têm limitações
- A bateria do celular será consumida mais rapidamente com GPS ativo
- Teste sempre em um Android físico para resultados reais
- O PC pode não ter GPS - simule dados no campo de entrada manual

## 🛠️ Desenvolvimento

### Para modificar a interface

Edite `templates/index.html` - as mudanças refletem automaticamente

### Para adicionar novos campos

1. Adicione campo no HTML
2. Atualize a função `saveLocation()` em JavaScript
3. Atualize a tabela do banco de dados se necessário

## 📞 Troubleshooting

### "Permissão negada ao capturar GPS"
- Verifique se está usando HTTPS (local pode usar HTTP)
- Permita acesso no navegador
- Ative GPS no dispositivo

### "Geolocalização não suportada"
- Use Chrome, Firefox ou Edge
- Safari pode ter restrições
- Verifique compatibilidade do navegador

### "Erro ao conectar"
- Verifique o firewall
- Certifique-se que Flask está rodando
- Use o IP correto (ipconfig no Windows)

## 📄 Licença

MIT - Livre para uso e modificação

---

**Desenvolvido com ❤️ usando Flask e Python**

# app-lat-long
