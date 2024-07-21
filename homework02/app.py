from flask import Flask, render_template, url_for, request, redirect, make_response

app = Flask(__name__)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect(url_for('greeting')))
        response.set_cookie('name', name)
        response.set_cookie('email', email)
        return response

    return render_template('form.html')


@app.route('/greeting/', methods=['GET', 'POST'])
def greeting():
    if request.method == 'POST':
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('name')
        response.delete_cookie('email')
        return response

    _name = request.cookies.get('name')
    context = {
        'name': _name
    }
    return render_template('greeting.html', **context)