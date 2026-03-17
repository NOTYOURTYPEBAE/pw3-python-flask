
from flask import Flask,render_template

#importando o controller
from controllers import routes

app = Flask(__name__, template_folder='views')

#Models:Manipulação dos dados do sistema
#Views:Interação com os usuários
#Controllers:Tratar as requisições. Camadas de controle
#request:requisição. Requisição http

#Enviando a variavel app para as rotas
routes.init_app(app)

#iniciando o servidor na porta 5000
if __name__ == '__main__':
    #verificando se o arquivo gravado em main é o arqivo principal
    app.run(port=5000, debug=True)
#o metodo .run() inicia o seu servidor