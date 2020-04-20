from datetime import timedelta

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Post, Message
from sanansaattaja.db.data.models.user import User
from sanansaattaja.website.forms import LoginForm, RegisterForm
from sanansaattaja.website.forms.message_form import MessageForm
from sanansaattaja.website.forms.post_form import PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sanansaattaja_secret_key'
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
    posts = db.query(Post).filter(Post.is_public == True).all()
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

@app.route('/private')
@login_required
def messages():
    db = db_session.create_session()
    messages = db.query(Message).filter((Message.author_id == current_user.id) | (Message.addressee_id == current_user.id)).all()
    return render_template('private.html', messages=messages)


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
                                   message="There is no such user")

        return redirect('/private')
    return render_template('message.html', title='Sending message', form=form)


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
        return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords are different")
        db = db_session.create_session()
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="This email is already used")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


db_session.global_init('sanansaattaja/db/sanansaattaja.db')
def run():
    # port = int(os.environ.get('PORT', 8080))
    # app.run(host='0.0.0.0', port=port, debug=False)
    app.run(port=8080, host='127.0.0.1')
