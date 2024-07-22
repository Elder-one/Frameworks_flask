from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=16)])
    confirm_pswd = PasswordField('Подтв. пароль',
                                 validators=[DataRequired(), EqualTo('password')])