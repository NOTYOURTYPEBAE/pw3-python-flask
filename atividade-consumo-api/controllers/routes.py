from flask import render_template
import requests

def init_app(app):
    
    @app.route('/')
    @app.route('/apilivros')
    def apilivros():
        livros = []
        mensagem = ''
        
        try:
            # Busca livros da autora Freida McFadden
            query = "Freida McFadden"
            url = f"https://openlibrary.org/search.json?q={query}&limit=20"
            response = requests.get(url)
            response.raise_for_status()
            
            dados = response.json()
            
            # Processando os resultados
            for doc in dados.get('docs', []):
                isbn_list = doc.get('isbn', [])
                isbn = isbn_list[0] if isbn_list else ''
                olid = doc.get('key', '').replace('/books/', '') if doc.get('key') else ''
                cover_id = doc.get('cover_i', '')
                title = doc.get('title', '')
                
                livro = {
                    'titulo': title,
                    'autor': ', '.join(doc.get('author_name', ['Autor não disponível'])),
                    'ano': doc.get('first_publish_year', 'Ano não disponível'),
                    'editora': ', '.join(doc.get('publisher', ['Editora não disponível'])),
                    'isbn': isbn,
                    'olid': olid,
                    'cover_id': cover_id,
                    'capa_1': f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else '',
                    'capa_2': f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg" if isbn else '',
                    'capa_3': f"https://covers.openlibrary.org/b/olid/{olid}-L.jpg" if olid else '',
                    'capa_4': f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else '',
                    'capa_fallback': f"https://placehold.co/400x600/667eea/white?text={title.replace(' ', '+')}"
                }
                livros.append(livro)
            
            mensagem = f'📚 {len(livros)} livros da Freida McFadden disponíveis'
            
        except Exception as e:
            mensagem = f'Erro ao carregar livros: {str(e)}'
        
        return render_template('apilivros.html', 
                             livros=livros, 
                             mensagem=mensagem)