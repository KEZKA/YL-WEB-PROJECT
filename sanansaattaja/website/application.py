import io
import os

from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Post, Message
from sanansaattaja.db.data.models.user import User
from sanansaattaja.website.forms import LoginForm, RegisterForm
from sanansaattaja.website.forms.message_form import MessageForm
from sanansaattaja.website.forms.post_form import PostForm
from sanansaattaja.core.utils import fullname, load_image, photos

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/')
def index():
    db = db_session.create_session()
    posts = db.query(Post).filter(Post.is_public is True).all()
    return render_template('main.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        post = Post()
        post.topic = form.topic.data
        post.text = form.text.data
        post.is_public = form.is_public.data
        current_user.posts.append(post)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('post.html', title='Публикация поста', form=form)


@app.route('/add_message', methods=['GET', 'POST'])
@login_required
def add_message():
    form = MessageForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        message = Message()
        message.text = form.text.data
        addressee = session.query(User).filter(User.email == message.addressee.data)
        if addressee:
            message.addressee_id = addressee.id
            addressee.received_messages.append(message)
        else:
            return render_template('message.html', title='Отправка сообщение', form=form,
                                   message="Такого пользователя не существует")
        current_user.messages.append(message)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('message.html', title='Публикация поста', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form,
                                   message="Такого пользователя не существует")
        if user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=login_form, message="Неверный пароль")
    else:
        return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db = db_session.create_session()
            if db.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Почта уже используется")
            if request.files['photo']:
                file = request.files['photo'].read()
            else:
                with open(load_image(
                        f"{'male' if form.sex.data == 'male' else 'female'}.jpg"),
                        mode='rb') as image:
                    print(load_image(f"{'male' if form.sex.data == 'male' else 'female'}.jpg"))
                    file = image.read()

            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                sex=form.sex.data,
                profile_picture=file
            )
            user.set_password(form.password.data)
            db.add(user)
            db.commit()
            return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user_page')
@login_required
def user_page():
    return send_file(io.BytesIO(current_user.profile_picture), mimetype='image/*')


db_session.global_init(fullname('db/sanansaattaja.db'))


# @app.route('/get_image')
# @login_required
# def get_image():
    # name = randint(10 ** 20, 10 ** 21 - 1)
    # with open(load_image(f'{name}.jpg'), mode='wb') as file:
    #     file.write(current_user.profile_picture)
    # return render_template('user_page.html', filename=name, current_user=current_user)
    # db = db_session.create_session()
    # user_data = db.query(User).filter(User.email == user.email).first()
    # return send_file(io.BytesIO(current_user.profile_picture), mimetype='image/*')


def run():
    # port = int(os.environ.get('PORT', 8080))
    # app.run(host='0.0.0.0', port=port, debug=False)
    app.run(port=8080, host='127.0.0.1')
