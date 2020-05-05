import io
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sanansaattaja.core.errors import PostError
from sanansaattaja.core.utils import load_image, fullname
from sanansaattaja.db.data import db_session
from sanansaattaja.db.servicees import message_service, post_service, user_service
from sanansaattaja.website.forms import LoginForm, RegisterForm, MessageForm, PostForm, FilterForm, EditProfileForm, \
    PasswordChangeForm
from sanansaattaja.website.utils import get_photo_from_request, get_data_from_filter_form_to_params

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
MAX_FILE_SIZE = 1024 ** 2

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return user_service.get_user_by_id(user_id)
    except Exception:
        return None


@app.route('/')
def index():
    posts = post_service.get_all_public_posts()
    return render_template('main.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post_service.append_post(form, current_user.id)
            return redirect('/')
        except Exception as e:
            return render_template('post.html', title='Post publishing', form=form, message=str(e), width=800)
    return render_template('post.html', title='Post publishing', form=form, width=800)


@app.route('/private')
@login_required
def private():
    try:
        messages = message_service.get_all_user_messages(current_user.id)
        return render_template('private.html', messages=messages, width=800)
    except Exception as e:
        return render_template('private.html', messages=[], message=str(e), width=800)


@app.route('/add_message', methods=['GET', 'POST'])
@login_required
def add_message():
    form = MessageForm()
    if form.validate_on_submit():
        try:
            message_service.append_message(form, current_user.id)
            return redirect(url_for('private'))
        except Exception as e:
            return render_template('message.html', title='Sending message', form=form, message=str(e), width=800)
    else:
        email = request.args.get('email')
        if email:
            return render_template('message.html', title='Sending message', form=form, width=800, addressee=email)
        return render_template('message.html', title='Sending message', form=form, width=800, addressee="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            user = user_service.get_user_by_email(login_form.email.data)
            user_service.password_verification(user, login_form.password.data)
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))

        except Exception as e:
            return render_template('login.html', form=login_form, message=str(e))

    else:
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
            user_service.add_user(form, file)
            return redirect('/login?register-success=true')
        except Exception as e:
            return render_template('register.html', title='Registration', form=form, message=str(e))
    return render_template('register.html', title='Registration', form=form)


@app.route('/edit_page', methods=['GET', 'POST'])
@login_required
def edit_page():
    form = EditProfileForm()
    password_form = PasswordChangeForm()
    if form.validate_on_submit():
        try:
            file = get_photo_from_request(request)
            if file is None and form.check_deletion.data != 'delete':
                file = current_user.profile_picture
            user_service.edit_user(current_user.id, form, file)
            return redirect('edit_page')
        except Exception as e:
            return render_template('edit_page.html', current_user=current_user, title='Edit page',
                form=form, password_form=password_form, message=str(e))
    if password_form.validate_on_submit():
        try:
            user_service.password_verification(current_user, password_form.old_password.data, changing=True)
            user_service.edit_password(current_user.id, password_form)
            return redirect('edit_page')
        except Exception as e:
            return render_template('edit_page.html', current_user=current_user, title='Edit page',
                form=form, password_form=password_form, message=str(e))
    return render_template('edit_page.html', current_user=current_user, title='Edit page', form=form,
        password_form=password_form)


@app.route('/make_image')
@login_required
def make_image():
    user_id = request.args.get('user_id')
    user = user_service.get_user_by_id(user_id)
    if not user.profile_picture:
        with open(load_image(f"{user.sex}.jpg"), mode='rb') as image:
            return send_file(io.BytesIO(image.read()), mimetype='image/*')
    return send_file(io.BytesIO(user.profile_picture), mimetype='image/*')


@app.route('/user_posts/<int:user_id>')
@login_required
def user_posts(user_id):
    try:
        post_id = request.args.get('post_id')
        if post_id:
            try:
                post_service.delete_post(post_id)
            except PostError:
                pass
        user = user_service.get_user_by_id(user_id)
        posts = post_service.get_all_user_posts(user_id)
        return render_template('user_posts.html', posts=posts, user=user)
    except Exception as e:
        return render_template('main.html', posts=[], message=str(e))


@app.route('/notes')
@login_required
def notes():
    try:
        post_id = request.args.get('post_id')
        if post_id:
            try:
                post_service.delete_post(post_id)
            except PostError:
                pass
        notes = post_service.get_user_notes(current_user.id)
        return render_template('notes.html', notes=notes)
    except Exception as e:
        return render_template('notes.html', notes=[], message=str(e))


@app.route('/users')
@login_required
def users():
    is_filter = request.args.get('filter')
    if is_filter:
        users = user_service.get_filer_users(request.args)
    else:
        users = user_service.get_users()
    return render_template('all_users.html', users=users)


@app.route('/users_filter', methods=['GET', 'POST'])
@login_required
def users_filter():
    form = FilterForm()
    if request.method == 'POST':
        try:
            params = get_data_from_filter_form_to_params(form)
            return redirect(f'/users?{params}')
        except Exception as e:
            return render_template('user_filter.html', form=form, message=str(e))
    return render_template('user_filter.html', form=form)


db_session.global_init(fullname('db/sanansaattaja.db'))


@app.route('/info/about')
def info():
    try:
        return render_template('info.html')
    except Exception as e:
        return render_template('info.html', message=str(e))


@app.route('/info/faq')
def faq():
    try:
        return render_template('faq.html')
    except Exception as e:
        return render_template('faq.html', message=str(e))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', text="page not found")


@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', text="you don't have access to this page")


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', text="oops something went wrong")


def run():
    port = int(os.environ.get('PORT', 8080))
    localhost = '127.0.0.1'
    globalhost = '0.0.0.0'

    # change host before deploying on heroku
    app.run(host=localhost, port=port, debug=False)
