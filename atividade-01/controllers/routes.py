from flask import render_template, request,redirect, url_for


def init_app(app):
    listaLivros=[{
'livro':'Melhor do que nos filmes',
'genero':'Romance',
'autor':'Lynn Painter'
    }]
    
    listaEditoras=[
        'Companhia das Letras',
        'Grupo Editorial Record',
        'Sextante',
        'Intrínseca'
    ]
    
    lista_editoras = [
    {"nome": "Companhia das Letras"},
    {"nome": "Editora Abril"},
    {"nome": "Saraiva"}
]
    
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/lista', methods=['GET','POST'])
    def lista():
        
        
        return render_template('lista.html',
                               listaLivros=listaLivros)

    @app.route('/formulario', methods=['GET', 'POST'])
    def formulario():
        
        if request.method=='POST':
                    
                    listaLivros.append({'livro':request.form.get('livro'),'genero':request.form.get('genero'),'autor':request.form.get('autor')})
                    return redirect(url_for('lista'))
        
        
        return render_template('formulario.html')
    
    @app.route("/editoras")
    def listar_editoras():
        
        return render_template("editoras.html", listaEditoras=lista_editoras)