from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import json
import os

app = Flask(__name__)
DB_FILE = "locations.db"

# ==================== BANCO DE DADOS ====================
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

# ==================== ROTAS ====================

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/save-location', methods=['POST'])
def save_location():
    """API para salvar localização"""
    try:
        data = request.json
        salvar_localizacao(
            data['latitude'],
            data['longitude'],
            data.get('altitude', 0),
            data.get('speed', 0),
            data.get('accuracy', 0),
            data.get('user_name', 'Anônimo'),
            data.get('description', '')
        )
        return jsonify({'success': True, 'message': 'Localização salva com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/get-locations', methods=['GET'])
def get_locations():
    """API para obter todas as localizações"""
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM locations ORDER BY timestamp DESC")
        columns = [description[0] for description in cursor.description]
        locations = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return jsonify(locations)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/delete-location/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """API para deletar uma localização"""
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
