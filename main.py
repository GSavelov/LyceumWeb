import os

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.groups import Group, Quest_groups
from data.exercises import Exercise
from forms.user import RegisterForm, LoginForm
from forms.exercise import ExerciseForm, GroupForm
from sqlalchemy import insert
from dotenv import load_dotenv
import groups_api

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    groups = db_sess.query(Group).all()
    return render_template("index.html", groups=groups)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_que', methods=['GET', 'POST'])
@login_required
def add_que():
    form = ExerciseForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        exercise = Exercise(question=form.question.data, answer=form.answer.data, user_id=current_user.id)
        db_sess.add(exercise)
        db_sess.commit()
        return render_template('add_que.html', title='Добавить вопрос', form=form, message='Вопрос успешно добавлен')
    return render_template('add_que.html', title='Добавить вопрос', form=form)


@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    form = GroupForm()
    db_sess = db_session.create_session()
    questions = db_sess.query(Exercise).filter(Exercise.user_id == current_user.id).all()
    # form.picks.data - список id
    # form.name.data - название (строка)
    form.picks.choices = [(que.id, que.question) for que in questions]
    if form.validate_on_submit():
        group = Group(name=form.name.data, user_id=current_user.id)
        db_sess.add(group)
        db_sess.commit()
        identifier = len(db_sess.query(Group).all())
        for q in form.picks.data:
            stmt = insert(Quest_groups).values(question_id=q, group_id=identifier)
            db_sess.execute(stmt)
            db_sess.commit()
        return redirect("/")
    return render_template('add_group.html', title='Добавить группу', form=form, questions=questions)


def main():
    db_session.global_init('db/learners.sqlite')
    app.register_blueprint(groups_api.blueprint)
    app.run(port=5050)


if __name__ == '__main__':
    main()
