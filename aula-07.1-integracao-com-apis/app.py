
from flask import Flask,render_template

#Importando o PYMYSQL
import pymysql
#importando o mysqlalchemy e o model
from models.database import db, Game

#definindo nome para o banco
DB_NAME='thegames'


#importando o controller
from controllers import routes

app = Flask(__name__, template_folder='views')

#Passando o nome do banco para o flask
app.config['DATABASE_NAME']=DB_NAME
#Passando o endereço do banco para o flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql://root@localhost/{DB_NAME}'

#definindo uma chave secreta (flash messages e sessões)
app.config['SECRET_KEY'] = '1234'


#Models:Manipulação dos dados do sistema
#Views:Interação com os usuários
#Controllers:Tratar as requisições. Camadas de controle
#request:requisição. Requisição http

#Enviando a variavel app para as rotas
routes.init_app(app)

#iniciando o servidor na porta 5000
if __name__ == '__main__':
    #Conectando-se ao Mysql para conectar o banco de dados
    #Passando oos dados de conexão
    connection=pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

#tentando a conexão
try:
    with connection.cursor() as cursor:
        #enviando a query para criar o banco
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
        print("O banco de dados está criado")
except Exception as error:
    print(f'Ocorreu um erro ao criar o banco de dados!{error}')
    #fechando conexão
finally: 
    connection.close()

    #inicializando o flask-sqlalchemy
    db.init_app(app=app)
    #enviando a requisição para criar as tabelas
    with app.test_request_context():
        db.create_all()
    
    app.run(port=5000, debug=True)
#o metodo .run() inicia o seu servidor