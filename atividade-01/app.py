from flask import Flask,render_template
from controllers import routes

app = Flask(__name__, template_folder='views')


routes.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)