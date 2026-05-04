
from flask import render_template, request,redirect, url_for

from models.database import Game


# criando a função principal para incializar as rotas


def init_app(app):

        #variáveis globais
            listaConsoles=[
                    'Palystation 5',
                    'Xbox One',
                    'Super Nintendo',
                    'Atari',
                    '3DS'
                ]
            
            listaGames = [{'titulo':'CS-GO', 
                          'ano':2012, 
                          'categoria':'FPS-Online',
                          'plataforma':'PC(Windows)'}]

            @app.route('/')
            def home():
                return render_template('index.html')


            @app.route('/games')
            def games():
                # Criando variaveis para rota de games
                titulo = "Portal 2"
                ano = 2011
                categoria = "puzzle"
                # lista de jogadores(uma lista é um vetor/array)
                jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']

                # Enviando as variáveis para o html
                return render_template('games.html',
                                    titulo=titulo,
                                    ano=ano,
                                    categoria=categoria,
                                    jogadores=jogadores)


            @app.route('/consoles', methods=['GET', 'POST'])
            def consoles():
                # criando um objeto
                console = {'Nome': 'Playstation 2',
                        'Fabricante': 'Sony',
                        'Ano': 2000}
            
                
                #recebendo o valor do formulário
                if request.method=='POST':
                    if request.form.get('novoConsole'):
                        listaConsoles.append(request.form.get('novoConsole'))
                    
                    
                    
                return render_template('consoles.html',
                                    console=console,
                                    listaConsoles=listaConsoles)
                
                
            @app.route ('/cadgames', methods=['GET','POST'])
            def cadgames():
                #Recebendo os dados do formulario e enviando para a página
                #Verificando se a requisição do usuário é igual a post
                if request.method=='POST':
                     #Aqui ele irá gravar os dados na lista de jogos
                     listaGames.append({'titulo':request.form.get('titulo'), 'ano':request.form.get('ano'), 'categoria':request.form.get('categoria'), 'plataforma':request.form.get('plataforma')})
                     #Aqui o usuário será redirecionado para a página novamente
                     return redirect(url_for('cadgames'))
                     
                     
                return render_template('cadgames.html', listaGames=listaGames)
            #rota para o CRUD (estoque de jogos)
            @app.route('/estoque', methods=['GET','POST'])
            def estoque():
                
                #selecionando todos os jogos da tabela
                games= Game.query.all()
                
                return render_template('estoque.html',games=games)
            