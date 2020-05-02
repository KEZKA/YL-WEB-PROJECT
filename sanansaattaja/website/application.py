import io
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sanansaattaja.core.utils import load_image, get_photo_from_request, fullname
from sanansaattaja.db.data import db_session
from sanansaattaja.db.servicees.message_service import get_all_user_messages, append_message
from sanansaattaja.db.servicees.post_service import get_all_public_posts, append_post, get_all_user_posts, \
    get_user_notes
from sanansaattaja.db.servicees.user_service import add_user, get_user_by_id, get_user_by_email, \
    password_verification, edit_user
from sanansaattaja.website.forms import LoginForm, RegisterForm
from sanansaattaja.website.forms.message_form import MessageForm
from sanansaattaja.website.forms.post_form import PostForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
MAX_FILE_SIZE = 1024 ** 2

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/')
def index():
    posts = get_all_public_posts()
    return render_template('main.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        append_post(form, current_user)
        return redirect('/')
    return render_template('post.html', title='Post publishing', form=form, width=800)


@app.route('/private')
@login_required
def private():
    messages = get_all_user_messages(current_user)
    return render_template('private.html', messages=messages, width=800)


@app.route('/add_message', methods=['GET', 'POST'])
@login_required
def add_message():
    form = MessageForm()
    if form.validate_on_submit():
        try:
            append_message(form, current_user)
        except Exception as e:
            return render_template('message.html', title='Sending message', form=form, message=str(e), width=800)
        return redirect('/private')
    return render_template('message.html', title='Sending message', form=form, width=800)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            user = get_user_by_email(login_form.email.data)
            password_verification(user, login_form.password.data)
            login_user(user, remember=login_form.remember_me.data)
        except Exception as e:
            return render_template('login.html', form=login_form, message=str(e))

        return redirect(url_for('index'))
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
    if form.validate_on_submit():
        try:
            file = get_photo_from_request(request)
            add_user(form, file)
        except Exception as e:
            return render_template('register.html', title='Registration', form=form, message=str(e))
        return redirect('/login?register-success=true')
    return render_template('register.html', title='Registration', form=form)


@app.route('/edit_page', methods=['GET', 'POST'])
@login_required
def edit_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            file = get_photo_from_request(request)
            if file is None and form.check_deletion.data != 'delete':
                file = current_user.profile_picture
            edit_user(current_user, form, file)
        except Exception as e:
            return render_template('edit_page.html', current_user=current_user, title='Edit page', form=form, message=str(e))
        return redirect('edit_page')
    return render_template('edit_page.html', current_user=current_user, title='Edit page', form=form)


@app.route('/make_image')
@login_required
def make_image():
    if not current_user.profile_picture:
        with open(load_image(f"{current_user.sex}.jpg"), mode='rb') as image:
            return send_file(io.BytesIO(image.read()), mimetype='image/*')
    return send_file(io.BytesIO(current_user.profile_picture), mimetype='image/*')

@app.route('/user_posts/<int:user_id>')
@login_required
def user_posts(user_id):
    posts = get_all_user_posts(user_id)
    print(posts)
    user = get_user_by_id(user_id)
    return render_template('user_posts.html', posts=posts, user=user)

@app.route('/notes')
@login_required
def notes():
    notes = get_user_notes(current_user.id)
    return render_template('notes.html', notes=notes)


db_session.global_init(fullname('db/sanansaattaja.db'))


def run():
    port = int(os.environ.get('PORT', 8080))
    localhost = '127.0.0.1'
    globalhost = '0.0.0.0'

    # change host before deploying on heroku
    app.run(host=localhost, port=port, debug=False)
