from flask import Flask
from controllers import routes

app = Flask(__name__, template_folder='views')

# Inicializa as rotas (onde está a view de consumo da API)
routes.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)