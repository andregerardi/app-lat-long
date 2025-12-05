# 🏘️ Seleção de Município e Agente - Guia de Uso

## ✨ O Que Foi Adicionado

### Antes:
- ❌ Campo de texto para nome/identificador
- ❌ Entrada manual de dados

### Depois:
- ✅ Caixa suspensa com 8 municípios
- ✅ Caixa suspensa dinâmica com agentes
- ✅ Interface intuitiva e responsiva
- ✅ Dados carregados do arquivo `agentes.xlsx`

---

## 📊 Dados Carregados

### Municípios e Agentes:

| Município | Quantidade de Agentes |
|-----------|----------------------|
| Barueri | 3 |
| Cabreúva | 3 |
| Campinas | 3 |
| Embu das Artes | 5 |
| Itaquaquecetuba | 10 |
| Paulínia | 2 |
| São Roque | 1 |
| São Vicente | 6 |

**Total: 33 agentes**

---

## 🎯 Como Usar

### 1️⃣ Selecione o Município
```
🏘️ Município
├─ Barueri
├─ Cabreúva
├─ Campinas
├─ Embu das Artes
├─ Itaquaquecetuba
├─ Paulínia
├─ São Roque
└─ São Vicente
```

### 2️⃣ Selecione o Agente
Após escolher o município, a lista de agentes será atualizada automaticamente:

**Exemplo - Itaquaquecetuba:**
```
👤 Agente
├─ Ana Carla Piepenbrink Lemes de Moura
├─ Arlene Martins De Jesus
├─ Arlete Tamandaré Mariniello
├─ Cleiton Vinicius da Rosa
├─ Eliane Lopes Niz
├─ Ioná Maria de Lima
├─ Luciana Ivone da Silva Oliveira
├─ Pedro Santos do Carmo
├─ Ryane Costa Vitorino Pereira da Silva
└─ Viviane Ferreira de andrade
```

### 3️⃣ O Nome Será Salvo
Quando você clicar em "💾 Salvar Localização", o nome do agente será registrado!

---

## 📁 Arquivos Criados

```
📂 Georeferenciamento/
├── 📄 gerar_agentes.py               ← Script para gerar dados do Excel
├── 📄 municipios_agentes.json        ← Dados em JSON (raiz)
├── 📂 static/
│   └── 📄 municipios_agentes.json    ← Dados em JSON (para web)
└── templates/
    └── 📄 index.html                 ← Interface atualizada
```

---

## 🔄 Como Atualizar os Dados

Se você adicionar ou modificar agentes no arquivo `agentes.xlsx`:

### Passo 1: Execute o Script
```bash
python gerar_agentes.py
```

### Passo 2: O arquivo será regenerado automaticamente
```
✅ Arquivo municipios_agentes.json criado!
```

### Passo 3: Reinicie o servidor Flask
```bash
python app_flask.py
```

---

## 💻 Tecnicamente

### Como Funciona:

1. **Carregamento de Dados:**
   - JavaScript faz fetch de `/static/municipios_agentes.json`
   - Dados carregam quando a página abre

2. **Seleção Dinâmica:**
   - Quando município muda, agentes são carregados
   - Usa `atualizarAgentes()` para atualizar lista

3. **Salvamento:**
   - Nome do agente selecionado é salvo no banco
   - Junto com localização e outros dados

---

## 🎨 Interface

### Desktop:
```
┌──────────────────────────┐
│  🏘️ Município             │
│  [Selecione um...]  ▼     │
└──────────────────────────┘

┌──────────────────────────┐
│  👤 Agente               │
│  [Selecione o agente...]  │  ← Atualiza dinamicamente
└──────────────────────────┘
```

### Mobile:
```
Mesmo layout, totalmente responsivo
Funciona perfeito em Android!
```

---

## 🔌 API e Banco de Dados

### O que é Salvo:

```json
{
  "id": 1,
  "latitude": -23.550520,
  "longitude": -46.633309,
  "user_name": "Ana Carla Piepenbrink Lemes de Moura",
  "description": "Ponto de coleta",
  "timestamp": "2025-12-05T...",
  ...
}
```

---

## ✅ Próximos Passos

1. **Teste Localmente:**
   ```bash
   python app_flask.py
   # Abra http://localhost:5000
   ```

2. **Teste a Seleção:**
   - Escolha um município
   - Veja os agentes aparecerem
   - Selecione um agente

3. **Teste o Deploy:**
   - Siga `DEPLOY_PASSO_A_PASSO.md`
   - Seu app estará online com a nova funcionalidade!

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| Dropdown vazio | Verifique se JSON está em `/static/` |
| Agentes não aparecem | Recarregue a página ou limpe cache |
| Erro no console | Veja logs do Flask |
| Dados não salvam | Verifique banco de dados SQLite |

---

## 📞 Suporte

- **Script não funciona:** `pip install openpyxl`
- **JSON não carrega:** Verifique caminho `/static/municipios_agentes.json`
- **Deploy não funciona:** Confirme que pasta `static/` está no repositório

---

**Desenvolvido com ❤️ para facilitar a seleção de agentes por município**

Pronto para usar! 🚀
