import os
from app_flask import app

# Configurar porto dinamicamente (importante para deploy)
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
