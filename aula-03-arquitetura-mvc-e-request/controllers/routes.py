
from flask import render_template, request



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

            @app.route('/')
            def home():
                return render_template('index.html')


            @app.route('/games')
            def games():
                # Criando variaveis para ropta de games
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
