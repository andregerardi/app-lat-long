import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

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
st.title("📍 Capturador de Localização GPS")
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
    
    # Script JavaScript para capturar localização do navegador
    location_script = """
    <script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const alt = position.coords.altitude || 0;
                const speed = position.coords.speed || 0;
                const accuracy = position.coords.accuracy;
                
                // Salvar em sessionStorage para Streamlit ler
                sessionStorage.setItem('gps_data', JSON.stringify({
                    latitude: lat,
                    longitude: lon,
                    altitude: alt,
                    speed: speed,
                    accuracy: accuracy,
                    timestamp: new Date().toISOString()
                }));
                
                // Disparar evento customizado
                window.dispatchEvent(new Event('gps_updated'));
            },
            function(error) {
                alert('Erro ao obter localização: ' + error.message);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert('Geolocalização não suportada neste navegador');
    }
    </script>
    """
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Pressione o botão abaixo para capturar sua localização:")
        # Capturar do navegador via JavaScript
        st.components.v1.html("""
            <button onclick="
                if (navigator.geolocation) {
                    document.getElementById('status').innerText = 'Capturando localização...';
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;
                            const alt = position.coords.altitude || 0;
                            const speed = position.coords.speed || 0;
                            const accuracy = position.coords.accuracy;
                            
                            document.getElementById('lat').value = lat;
                            document.getElementById('lon').value = lon;
                            document.getElementById('alt').value = alt;
                            document.getElementById('speed').value = speed;
                            document.getElementById('acc').value = accuracy;
                            
                            document.getElementById('status').innerHTML = 
                                '<span style=\"color: green;\"><b>✓ Localização capturada!</b></span>';
                        },
                        function(error) {
                            document.getElementById('status').innerHTML = 
                                '<span style=\"color: red;\"><b>✗ Erro: ' + error.message + '</b></span>';
                        },
                        {enableHighAccuracy: true, timeout: 10000, maximumAge: 0}
                    );
                }
            " style="
                width: 100%;
                padding: 15px;
                font-size: 18px;
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: bold;
            ">
            📍 CAPTURAR LOCALIZAÇÃO
            </button>
            <div id="status" style="margin-top: 10px; font-size: 14px;"></div>
            
            <input type="hidden" id="lat">
            <input type="hidden" id="lon">
            <input type="hidden" id="alt">
            <input type="hidden" id="speed">
            <input type="hidden" id="acc">
        """, height=100)
    
    # Campos para entrada manual (backup)
    st.markdown("### Ou insira manualmente:")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude:", format="%.6f", step=0.000001)
    with col2:
        lon = st.number_input("Longitude:", format="%.6f", step=0.000001)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        alt = st.number_input("Altitude (m):", format="%.2f")
    with col2:
        speed = st.number_input("Velocidade (m/s):", format="%.2f")
    with col3:
        accuracy = st.number_input("Precisão (m):", format="%.2f")
    
    description = st.text_area("📝 Descrição/Observações:", placeholder="Adicione informações sobre este ponto...")
    
    # Botão de salvar
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Salvar Localização", key="save_btn"):
            if lat == 0 and lon == 0:
                st.error("❌ Por favor, defina latitude e longitude válidas!")
            else:
                salvar_localizacao(lat, lon, alt, speed, accuracy, user_name or "Anônimo", description)
                st.success("✅ Localização salva com sucesso!")
                st.balloons()
    
    with col2:
        if st.button("🔄 Limpar Campos"):
            st.rerun()
    
    # Exibir mapa com a localização atual
    if lat != 0 and lon != 0:
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
