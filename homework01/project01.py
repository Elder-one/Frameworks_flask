from flask import Flask
from flask import url_for
from flask import render_template

app = Flask(__name__)

@app.route('/main/')
def main():
    return 'Ахахахахахахха'

@app.route('/categories/')
def categories():
    _category_list = [
        {
            'func_name': 'main',
            'img': 'jacket_category.jpg',
            'name': 'Куртки'
        },
        {
            'func_name': 'main',
            'img': 'hat_category.jpg',
            'name': 'Головные уборы'
        },
        {
            'func_name': 'main',
            'img': 'wig_category.jpg',
            'name': 'Парики'
        }
    ]
    context = {'category_list': _category_list}
    return render_template('categories.html', **context)