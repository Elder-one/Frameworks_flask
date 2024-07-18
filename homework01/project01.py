from flask import Flask
from flask import url_for
from flask import render_template

app = Flask(__name__)


@app.route('/main/')
def main():
    return render_template('main.html')


@app.route('/categories/')
def categories():
    _category_list = [
        {
            'cat_name': 'jackets',
            'img': 'jacket_category.jpg',
            'name': 'Куртки'
        },
        {
            'cat_name': 'hats',
            'img': 'hat_category.jpg',
            'name': 'Головные уборы'
        },
        {
            'cat_name': 'wigs',
            'img': 'wig_category.jpg',
            'name': 'Парики'
        }
    ]
    context = {'category_list': _category_list}
    return render_template('categories.html', **context)


@app.route('/categories/<category_name>/')
def category(category_name):
    _items = []
    if category_name == 'jackets':
        _items = [
            {
                'page_name': 'jacket01',
                'name': 'Jacket 01',
                'img': 'jacket01.jpg'
            },
            {
                'page_name': 'jacket02',
                'name': 'Jacket 02',
                'img': 'jacket02.jpg'
            }
        ]
    elif category_name == 'hats':
        _items = [
            {
                'page_name': 'hat01',
                'name': 'Hat 01',
                'img': 'hat01.jpg'
            }
        ]
    elif category_name == 'wigs':
        _items = []

    _cat_name = 'unknown'
    if category_name == 'wigs':
        _cat_name = 'парики'
    elif category_name == 'jackets':
        _cat_name = 'куртки'
    elif category_name == 'hats':
        _cat_name = 'головные уборы'

    context = {'items': _items,
               'cat_name': _cat_name}

    return render_template('category.html', **context)


@app.route('/item-page/<page_name>')
def item_page(page_name):
    _item = {
        'name': None,
        'img': None,
        'desc': ('Lorem ipsum dolor sit, '
                 'amet consectetur adipisicing elit. '
                 'Debitis repellendus impedit aspernatur '
                 'doloremque assumenda. Recusandae in '
                 'ratione alias sapiente et possimus '
                 'autem exercitationem, ipsam nemo suscipit '
                 'nisi dolorem similique eveniet repellendus '
                 'dicta laudantium deleniti debitis quasi, '
                 'iste nam quaerat quisquam vel tenetur quia! '
                 'Deserunt adipisci est asperiores '
                 'doloremque quae eius.')
    }
    if page_name == 'jacket01':
        _item['img'] = 'jacket01.jpg'
        _item['name'] = 'Jacket 01'
    elif page_name == 'jacket02':
        _item['img'] = 'jacket02.jpg'
        _item['name'] = 'Jacket 02'
    elif page_name == 'hat01':
        _item['img'] = 'hat01.jpg'
        _item['name'] = 'Hat 01'

    context = {'item': _item}
    return render_template('item-page.html', **context)
