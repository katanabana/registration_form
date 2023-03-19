from flask import Flask, render_template, request, redirect
from data.jobs import Jobs
from data.users import User
from data.db_session import global_init, create_session
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('index.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        global_init('db/database.db')
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('index.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.address = form.address.data
        user.set_password(form.password.data)
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('index.html', title='Регистрация', form=form)

@app.route('/login')
def login():
    return 'form submitted'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
