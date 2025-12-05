import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd
from urllib.parse import urlencode

# Configuração da página
st.set_page_config(
    page_title="📍 Capturador GPS",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos customizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== BANCO DE DADOS ====================
DB_FILE = "locations.db"

def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            altitude REAL,
            speed REAL,
            accuracy REAL,
            timestamp TEXT NOT NULL,
            user_name TEXT,
            description TEXT
        )
    """)
    conn.commit()
    return conn

def salvar_localizacao(lat, lon, alt, speed, accuracy, user_name, description):
    """Salva localização no banco de dados"""
    conn = init_db()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO locations (latitude, longitude, altitude, speed, accuracy, timestamp, user_name, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (lat, lon, alt, speed, accuracy, timestamp, user_name, description))
    conn.commit()
    conn.close()
    return True

def obter_localizacoes():
    """Retorna todas as localizações salvas"""
    conn = init_db()
    df = pd.read_sql_query("SELECT * FROM locations ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def deletar_localizacao(location_id):
    """Deleta uma localização do banco"""
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
    conn.commit()
    conn.close()

# ==================== ESTADO DA SESSÃO ====================
if 'location_captured' not in st.session_state:
    st.session_state.location_captured = False
    st.session_state.latitude = None
    st.session_state.longitude = None
    st.session_state.altitude = None
    st.session_state.speed = None
    st.session_state.accuracy = None

# ==================== INTERFACE ====================
st.title("📍 Localizador Superação")
st.markdown("Capture a localização do seu dispositivo Android em tempo real")

# Inicializar banco de dados
init_db()

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    user_name = st.text_input("👤 Seu nome/ID:", placeholder="Digite seu identificador")
    
    tab1, tab2, tab3 = st.tabs(["📍 Capturar", "📊 Histórico", "ℹ️ Sobre"])

with tab1:
    st.header("Capturar Localização")
    
    st.markdown("### 📍 Capture sua Localização")
    st.info("⚠️ **IMPORTANTE**: Certifique-se de que o GPS está ATIVADO no seu Android e permita acesso ao site!")
    
    # Inicializar state para armazenar dados GPS
    if 'gps_lat' not in st.session_state:
        st.session_state.gps_lat = 0.0
        st.session_state.gps_lon = 0.0
        st.session_state.gps_alt = 0.0
        st.session_state.gps_speed = 0.0
        st.session_state.gps_accuracy = 0.0
        st.session_state.gps_captured = False
    
    # HTML/JavaScript para capturar GPS usando localStorage
    st.components.v1.html("""
    <div style="text-align: center; padding: 20px;">
        <button id="captureBtn" style="
            width: 100%;
            max-width: 300px;
            padding: 20px;
            font-size: 18px;
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;
        " onmouseover="this.style.boxShadow='0 6px 12px rgba(0,0,0,0.2)'" 
           onmouseout="this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)'">
            📍 CAPTURAR LOCALIZAÇÃO
        </button>
        <div id="status" style="margin-top: 15px; font-size: 16px; min-height: 30px;"></div>
        <div id="coords" style="margin-top: 15px; font-size: 14px; color: #666;"></div>
    </div>
    
    <script>
    function captureLocation() {
        const btn = document.getElementById('captureBtn');
        const status = document.getElementById('status');
        const coords = document.getElementById('coords');
        
        btn.disabled = true;
        btn.style.opacity = '0.7';
        status.innerHTML = '<span style="color: #0066cc;"><b>⏳ Capturando localização...</b></span>';
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const alt = position.coords.altitude || 0;
                    const speed = position.coords.speed || 0;
                    const accuracy = position.coords.accuracy || 0;
                    
                    // Salvar em localStorage
                    localStorage.setItem('gps_data', JSON.stringify({
                        lat: lat,
                        lon: lon,
                        alt: alt,
                        speed: speed,
                        accuracy: accuracy,
                        timestamp: new Date().toISOString()
                    }));
                    
                    status.innerHTML = '<span style="color: green;"><b>✓ Localização capturada!</b></span>';
                    coords.innerHTML = `<b>Latitude:</b> ${lat.toFixed(6)}<br><b>Longitude:</b> ${lon.toFixed(6)}<br><b>Precisão:</b> ±${accuracy.toFixed(0)}m`;
                    
                    // Trigger streamlit rerun
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                },
                function(error) {
                    let errorMsg = error.message;
                    if (error.code === error.PERMISSION_DENIED) {
                        errorMsg = 'Permissão negada! Ative o acesso ao GPS nas configurações do navegador.';
                    } else if (error.code === error.POSITION_UNAVAILABLE) {
                        errorMsg = 'Posição indisponível. Tente ativar o GPS.';
                    } else if (error.code === error.TIMEOUT) {
                        errorMsg = 'Tempo limite excedido. Tente novamente.';
                    }
                    
                    status.innerHTML = '<span style="color: red;"><b>✗ Erro: ' + errorMsg + '</b></span>';
                    btn.disabled = false;
                    btn.style.opacity = '1';
                },
                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0
                }
            );
        } else {
            status.innerHTML = '<span style="color: red;"><b>✗ Geolocalização não suportada neste navegador!</b></span>';
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    }
    
    // Adicionar listener ao botão
    document.getElementById('captureBtn').addEventListener('click', captureLocation);
    </script>
    """, height=200)
    
    # Verificar se há dados no localStorage
    st.components.v1.html("""
    <script>
    const gpsData = localStorage.getItem('gps_data');
    if (gpsData) {
        const data = JSON.parse(gpsData);
        window.streamlit_gps = {
            lat: data.lat,
            lon: data.lon,
            alt: data.alt,
            speed: data.speed,
            accuracy: data.accuracy
        };
    }
    </script>
    """, height=0)
    
    st.markdown("---")
    st.markdown("### Dados Capturados")
    
    # Campos com valores capturados
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude:", value=st.session_state.gps_lat, format="%.6f", step=0.000001, key="lat_input")
    with col2:
        lon = st.number_input("Longitude:", value=st.session_state.gps_lon, format="%.6f", step=0.000001, key="lon_input")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        alt = st.number_input("Altitude (m):", value=st.session_state.gps_alt, format="%.2f", key="alt_input")
    with col2:
        speed = st.number_input("Velocidade (m/s):", value=st.session_state.gps_speed, format="%.2f", key="speed_input")
    with col3:
        accuracy = st.number_input("Precisão (m):", value=st.session_state.gps_accuracy, format="%.2f", key="acc_input")
    
    description = st.text_area("📝 Descrição/Observações:", placeholder="Adicione informações sobre este ponto...", key="desc_input")
    
    # Botões de ação
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Salvar Localização", key="save_btn"):
            if lat == 0.0 and lon == 0.0:
                st.error("❌ Por favor, defina latitude e longitude válidas!")
            else:
                salvar_localizacao(lat, lon, alt, speed, accuracy, user_name or "Anônimo", description)
                st.success("✅ Localização salva com sucesso!")
                st.balloons()
    
    with col2:
        if st.button("🔄 Limpar Campos"):
            st.session_state.gps_lat = 0.0
            st.session_state.gps_lon = 0.0
            st.session_state.gps_alt = 0.0
            st.session_state.gps_speed = 0.0
            st.session_state.gps_accuracy = 0.0
            st.rerun()
    
    # Exibir mapa com a localização atual
    if lat != 0.0 and lon != 0.0:
        st.markdown("### 🗺️ Mapa da Localização")
        m = folium.Map(
            location=[lat, lon],
            zoom_start=15,
            tiles="OpenStreetMap"
        )
        
        # Adicionar marcador
        folium.Marker(
            location=[lat, lon],
            popup=f"Lat: {lat:.6f}, Lon: {lon:.6f}",
            tooltip="Localização capturada",
            icon=folium.Icon(color='blue', icon='location-dot')
        ).add_to(m)
        
        # Círculo de precisão
        if accuracy > 0:
            folium.Circle(
                location=[lat, lon],
                radius=accuracy,
                color='blue',
                fill=True,
                fillColor='lightblue',
                fillOpacity=0.3,
                popup=f"Precisão: ±{accuracy:.0f}m"
            ).add_to(m)
        
        st_folium(m, width=700, height=500)

with tab2:
    st.header("📊 Histórico de Localizações")
    
    df = obter_localizacoes()
    
    if len(df) > 0:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("Filtrar por usuário"):
                user_filter = st.selectbox("Usuário:", df['user_name'].unique())
                df = df[df['user_name'] == user_filter]
        
        with col2:
            if st.checkbox("Últimas N localizações"):
                n = st.number_input("Quantas?", min_value=1, value=5)
                df = df.head(n)
        
        # Exibir tabela
        st.dataframe(df[['timestamp', 'user_name', 'latitude', 'longitude', 'altitude', 'accuracy', 'description']], 
                     use_container_width=True)
        
        # Mapa com todas as localizações
        st.markdown("### 🗺️ Mapa com Todas as Localizações")
        m = folium.Map(
            location=[df['latitude'].mean(), df['longitude'].mean()],
            zoom_start=13,
            tiles="OpenStreetMap"
        )
        
        # Cores diferentes para cada usuário
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue']
        users = df['user_name'].unique()
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(users)}
        
        for idx, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['user_name']}</b><br>{row['timestamp']}<br>{row['description']}",
                icon=folium.Icon(color=color_map[row['user_name']], icon='location-dot')
            ).add_to(m)
        
        st_folium(m, width=700, height=500)
        
        # Opções de exportação
        st.markdown("### 📥 Exportar Dados")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Baixar CSV",
                data=csv,
                file_name="localizacoes.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient='records', force_ascii=False, indent=2)
            st.download_button(
                label="📋 Baixar JSON",
                data=json_data,
                file_name="localizacoes.json",
                mime="application/json"
            )
        
        with col3:
            if st.button("🗑️ Limpar Histórico"):
                if st.checkbox("Confirmar exclusão de TODOS os dados"):
                    conn = init_db()
                    conn.execute("DELETE FROM locations")
                    conn.commit()
                    conn.close()
                    st.success("Histórico limpo!")
                    st.rerun()
    else:
        st.info("📭 Nenhuma localização capturada ainda. Volte à aba 'Capturar' para começar!")

with tab3:
    st.header("ℹ️ Informações")
    
    st.markdown("""
    ### 🚀 Como Usar
    
    1. **Acesse via Android**: Abra este aplicativo em um navegador no seu celular Android
    2. **Ative o GPS**: Certifique-se que o GPS está ativado no seu dispositivo
    3. **Permita Localização**: O navegador solicitará permissão para acessar sua localização
    4. **Clique no Botão**: Pressione "📍 CAPTURAR LOCALIZAÇÃO"
    5. **Salve os Dados**: Clique em "💾 Salvar Localização"
    
    ### 📊 Recursos
    
    - ✅ Captura de GPS em tempo real do Android
    - ✅ Visualização em mapa interativo (Folium)
    - ✅ Armazenamento em banco de dados SQLite
    - ✅ Histórico completo de localizações
    - ✅ Exportação para CSV e JSON
    - ✅ Múltiplos usuários
    - ✅ Precisão e altitude
    
    ### 🌐 Como Hospedar Online
    
    #### Opção 1: Streamlit Cloud (Recomendado - Gratuito)
    ```bash
    # 1. Crie conta em https://streamlit.io/cloud
    # 2. Conecte seu GitHub
    # 3. Faça deploy direto do seu repositório
    ```
    
    #### Opção 2: Heroku
    ```bash
    heroku create seu-app-gps
    git push heroku main
    ```
    
    #### Opção 3: PythonAnywhere
    ```bash
    # Visite https://www.pythonanywhere.com
    # Faça upload do código
    ```
    
    ### ⚠️ Notas Importantes
    
    - A localização será mais precisa se estiver ao ar livre
    - Alguns navegadores/dispositivos podem ter limitações de GPS
    - Os dados são salvos localmente (no servidor)
    - Use HTTPS para melhor compatibilidade
    
    ### 📱 Compatibilidade
    
    - ✅ Android 6.0+
    - ✅ iOS 14+
    - ✅ Qualquer navegador moderno (Chrome, Firefox, Edge, etc)
    """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido com ❤️ usando Streamlit e Python**")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📍 Total de Localizações", len(obter_localizacoes()))
with col2:
    try:
        total_users = len(obter_localizacoes()['user_name'].unique())
        st.metric("👥 Usuários Únicos", total_users)
    except:
        st.metric("👥 Usuários Únicos", 0)
with col3:
    st.metric("💾 Banco de Dados", "SQLite")
