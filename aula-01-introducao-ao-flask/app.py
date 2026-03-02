#Comentário no Python
#Importando o flask para aplicação

#Se usa flask minus. pq é o pacote e Flask maius. é uma classe
# e a partir do Flask eu posso usar as funções 
from flask import Flask,render_template
#carregando o Flask na variável "app"
app = Flask(__name__, template_folder='views')
#variáveis com __ são variáveisde ambiente do python
#__name__ representa o nome da aplicação


#criando a rota principal do site
# @ cria rota a função
@app.route('/')
#def cria funções no python
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    #Criando variaveis para ropta de games
    titulo="Portal 2"
    ano=2011
    categoria="puzzle"
    #lista de jogadores(uma lista é um vetor/array)
    jogadores=['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']
    
    
    #Enviando as variáveis para o html
    return render_template('games.html',
                           titulo=titulo,
                           ano=ano,
                           categoria=categoria,
                           jogadores=jogadores)
    

@app.route('/consoles')
def consoles():
    #criando um objeto
    console = {'Nome' : 'Playstation 2',
             'Fabricante' : 'Sony',
             'Ano' : 2000}
    
    
    return render_template('consoles.html',
                           console=console)


#iniciando o servidor na porta 5000
if __name__ == '__main__':
    #verificando se o arquivo gravado em main é o arqivo principal
    app.run(port=5000, debug=True)
#o metodo .run() inicia o seu servidor