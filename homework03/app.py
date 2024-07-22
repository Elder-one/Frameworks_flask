from hashlib import sha256
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from db_models import db, User
from forms import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = b'37b87056216c91400a2c04b3b5ebd9ad42cb905ae12159a22f662de1a1390a95'
csrf = CSRFProtect(app)
db.init_app(app)
app.app_context().push()
db.create_all()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if request.method == 'POST' and reg_form.validate():
        f_name = reg_form.first_name.data
        l_name = reg_form.last_name.data
        _email = reg_form.email.data
        _password = sha256(reg_form.password.data.encode('utf-8')).hexdigest()
        check = User.query.filter_by(email=_email).all()
        if check:
            return "Данный адрес уже есть в базе"
        user = User(first_name=f_name, last_name=l_name,
                    email=_email, password=_password)
        db.session.add(user)
        db.session.commit()
        print('OK')
        return 'Успешная регистрация'
    return render_template('registration.html', form=reg_form)
