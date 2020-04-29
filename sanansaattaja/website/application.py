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
from sanansaattaja.core.utils import fullname, load_image

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
MAX_FILE_SIZE = 1024 ** 2

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/')
def index():
    db = db_session.create_session()
    posts = db.query(Post).filter(Post.is_public == True).order_by(Post.modified_date.desc()).all()
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
    return render_template('post.html', title='Post publishing', form=form, width=800)


@app.route('/private')
@login_required
def messages():
    db = db_session.create_session()
    messages = db.query(Message).filter(
        (Message.author_id == current_user.id) | (Message.addressee_id == current_user.id)).order_by(
        Message.modified_date.desc()).all()
    return render_template('private.html', messages=messages, width=800)


@app.route('/add_message', methods=['GET', 'POST'])
@login_required
def add_message():
    form = MessageForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        addressee = session.query(User).filter(User.email == form.addressee.data).first()
        if addressee:
            message = Message()
            message.text = form.text.data
            message.author_id = current_user.id
            message.addressee_id = addressee.id
            session.add(message)
            session.commit()

        else:
            return render_template('message.html', title='Sending message', form=form,
                                   message="There is no such user", width=800)

        return redirect('/private')
    return render_template('message.html', title='Sending message', form=form, width=800)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form, message="There is no such user")
        if user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=login_form, message="Wrong password")
    else:
        print(request.args.get('register-success'))
        return render_template('login.html', form=login_form, success=True if request.args.get(
            'register-success') == 'true' else False)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords do not match")
        db = db_session.create_session()
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="This email is already in use")
        if request.files['photo']:
            filename = request.files['photo'].filename
            if filename.split('.')[-1].lower() not in ('jpg', 'png', 'gif'):
                return render_template('register.html', title='Registration',
                                       form=form,
                                       message="Invalid extension of image")
            file = request.files['photo'].read(MAX_FILE_SIZE)
            if len(file) == MAX_FILE_SIZE:
                return render_template('register.html', title='Registration',
                                       form=form,
                                       message="File size is too large")
        else:
            file = None

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            sex=form.sex.data,
            profile_picture=file
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()

        return redirect('/login?register-success=true')
    return render_template('register.html', title='Registration', form=form)


@app.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    form = RegisterForm()
    if request.method == 'POST':
        if request.files['photo']:
            print(form.photo.data.filename)
            filename = request.files['photo'].filename
            if filename.split('.')[-1].lower() not in ('jpg', 'png', 'gif'):
                return render_template('user_page.html', title='User page',
                                       form=form,
                                       message="Invalid extension of image")
            file = request.files['photo'].read(MAX_FILE_SIZE)
            if len(file) == MAX_FILE_SIZE:
                return render_template('user_page.html', title='User page',
                                       form=form,
                                       message="File size is too large")
        else:
            if form.check_deletion.data == 'delete':
                file = None
            else:
                file = current_user.profile_picture
        db = db_session.create_session()

        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.age = form.age.data
        current_user.sex = form.sex.data
        current_user.profile_picture = file

        db.merge(current_user)
        db.commit()
        return redirect('/user_page')
    return render_template('user_page.html', current_user=current_user, title='User page', form=form)


@app.route('/make_image')
@login_required
def make_image():
    if not current_user.profile_picture:
        with open(load_image(f"{current_user.sex}.jpg"), mode='rb') as image:
            return send_file(io.BytesIO(image.read()), mimetype='image/*')
    return send_file(io.BytesIO(current_user.profile_picture), mimetype='image/*')


db_session.global_init(fullname('db/sanansaattaja.db'))


def run():
    port = int(os.environ.get('PORT', 8080))
    localhost = '127.0.0.1'
    globalhost = '0.0.0.0'

    # change host before deploying on heroku
    app.run(host=globalhost, port=port, debug=False)
