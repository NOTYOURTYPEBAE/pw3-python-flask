
from flask import app, render_template, request, redirect, url_for, flash, session

# Importando o markupsafe (permite incluir links nas flash messages)
from markupsafe import Markup

from models.database import Game, db, Console, Usuario
# importando biblioteca werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import urllib.request
import json

# urllib é uma biblioteca nativa do python que permite fazer requisições http para consumir APIs
# json é uma biblioteca nativa do python que permite manipular dados no formato JSON
# "https://www.freetogame.com/api/games" url da api

# criando a função principal para incializar as rotas


def init_app(app):

        # variáveis globais
            listaConsoles = [
                    'Palystation 5',
                    'Xbox One',
                    'Super Nintendo',
                    'Atari',
                    '3DS'
                ]

            listaGames = [{'titulo': 'CS-GO',
                          'ano': 2012,
                          'categoria': 'FPS-Online',
                          'plataforma': 'PC(Windows)'}]

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

                # recebendo o valor do formulário
                if request.method == 'POST':
                    if request.form.get('novoConsole'):
                        listaConsoles.append(request.form.get('novoConsole'))

                return render_template('consoles.html',
                                    console=console,
                                    listaConsoles=listaConsoles)

            @app.route('/cadgames', methods=['GET', 'POST'])
            def cadgames():
                # Recebendo os dados do formulario e enviando para a página
                # Verificando se a requisição do usuário é igual a post
                if request.method == 'POST':
                     # Aqui ele irá gravar os dados na lista de jogos
                     listaGames.append({'titulo': request.form.get('titulo'), 'ano': request.form.get(
                         'ano'), 'categoria': request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
                     # Aqui o usuário será redirecionado para a página novamente
                     return redirect(url_for('cadgames'))

                return render_template('cadgames.html', listaGames=listaGames)
            # rota para o CRUD (estoque de jogos)

            @app.route('/estoque', methods=['GET', 'POST'])
            # adicionando o parâmetro id a rota
            @app.route('/estoque/delete/<int:id>')
            def estoque(id=None):
                # verificando se id foi passado para rota
                if id:
                    game = Game.query.get(id)  # seleciona jogo
                    db.session.delete(game)
                    db.session.commit()
                    return redirect(url_for('estoque'))

                # condição para verificar se o usuário está enviando uma requisição post (Cadastro)
                if request.method == 'POST':
                    # realiza o cadastro
                    # coletando os dados do usuário
                    # pega ps dados e transforma em um dicionário
                    dados = request.form.to_dict()
                    # enviando os dados para o model
                    newgame = Game(dados['titulo'], dados['ano'], dados['categoria'],
                                   dados['plataforma'], dados['preco'], dados['quantidade'])
                # método do sqlalchemy para gravar no banco
                    db.session.add(newgame)
                # confirmação
                    db.session.commit()
                    return redirect(url_for('estoque'))

                 # selecionando todos os jogos da tabela
                games = Game.query.all()
                return render_template('estoque.html', games=games)

            @app.route('/estoque_consoles', methods=['GET', 'POST'])
            def estoque_consoles():
                # condição para verificar se o usuário está enviando uma requisição post (Cadastro)
                if request.method == 'POST':
                    # realiza o cadastro
                    # coletando os dados do usuário
                    # pega ps dados e transforma em um dicionário
                    dados = request.form.to_dict()
                    # enviando os dados para o model
                    newconsole = Console(
                        dados['nome'], dados['fabricante'], dados['ano'], dados['preco'])
                # método do sqlalchemy para gravar no banco
                    db.session.add(newconsole)
                # confirmação
                    db.session.commit()
                    return redirect(url_for('estoque_consoles'))

                 # selecionando todos os jogos da tabela
                consoles = Console.query.all()
                return render_template('estoque_console.html', consoles=consoles)

            @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
            def editar(id):
                # Selecionando o jogo na banco pelo id
                game = Game.query.get(id)
                # verificando se a a quisição está post
                if request.method == 'POST':
                    dados_form = request.form.to_dict()
                    # alterando os dados do jogo
                    game.titulo = dados_form['titulo']
                    game.ano = dados_form['ano']
                    game.categoria = dados_form['categoria']
                    game.plataforma = dados_form['plataforma']
                    game.preco = dados_form['preco']
                    game.quantidade = dados_form['quantidade']
                    db.session.commit()
                    return redirect(url_for('estoque'))
                return render_template('editGame.html', game=game)

            @app.route('/cadastro', methods=['GET', 'POST'])
            def cadastro():
                if request.method == 'POST':
                    email = request.form['email']
                    senha = request.form['senha']
                    # verificando se o usuario já existe
                    usuario = Usuario.query.filter_by(email=email).first()
                    # verificando se a consulta retornou algo
                    if usuario:
                        msgUsuario = Markup(
                            "Usuário já cadastrado. Faça o <a href='/login'>login </a>")
                        flash(msgUsuario, 'danger')
                        return redirect(url_for('cadastro'))

                    # gerando o hash de senha (criptografia)
                    senha_com_hash = generate_password_hash(
                        senha, method='scrypt')

                    novo_usuario = Usuario(email=email, senha=senha_com_hash)
                    db.session.add(novo_usuario)
                    db.session.commit()

                    # gerando mensagem de sucesso
                    msgCad = Markup(
                        "Cadastro realizado com sucesso! Você já pode fazer o <a href='/login'>login</a>")
                    flash(msgCad, 'success')

                    return redirect(url_for('cadastro'))

                return render_template('cadastro.html')

            @app.route('/login', methods=['GET', 'POST'])
            def login():
                # verificando se o metodo é post
                if request.method == 'POST':
                    # coletando dados do formulario
                    email = request.form['email']
                    senha = request.form['senha']
                    # buscando o usuario pelo banco pelo email
                    usuario = Usuario.query.filter_by(email=email).first()
                    # se o usuario existir
                    if usuario:
                        # verificando a senha
                        if check_password_hash(usuario.senha, senha):
                            # aqui será criado a sessão
                            session['usuario_id'] = usuario.id
                            session['usuario_email'] = usuario.email
                            msgLogin = "Você foi autenticado com sucesso! Bem-vindo!"
                            flash(msgLogin, 'success')

                return render_template('login.html')

            # pacotes/ bibliotecas sistemas de login: werkzeug, flash, markup safe, session

    # Rota do consumo da APi
            @app.route('/apigames', methods=['GET', 'POST'])
            @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
            def apigames(id=None):
                # Variavel que armazena a url da API
                url = "https://www.freetogame.com/api/games"
                # Fazendo a requisição http para a API
                req = urllib.request.urlopen(url)
                # Lendo os dados da resposta
                dados = req.read()
                # Convertendo os dados para JSON
                listaJogos = json.loads(dados)
                if id:
                   jogoInfo = []
                   for jogo in listaJogos:
                        if jogo['id'] == id:
                            jogoInfo = jogo
                            break
                   if jogoInfo:
                       return render_template('jogoInfo.html', jogoInfo=jogoInfo)
                   else: 
                       return f'Game com a ID {id} não foi encontrada.'
                else:
                    return render_template('apigames.html', listaJogos=listaJogos)
