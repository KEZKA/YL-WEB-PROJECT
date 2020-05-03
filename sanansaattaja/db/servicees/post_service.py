from sqlalchemy.orm import selectinload

from sanansaattaja.core.errors import PostError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Post


def get_all_public_posts():
    session = db_session.create_session()
    posts = session.query(Post).options(selectinload(Post.author)).filter(Post.is_public == True).order_by(Post.modified_date.desc()).all()
    return posts


def get_all_user_posts(user_id):
    session = db_session.create_session()
    posts = session.query(Post).options(selectinload(Post.author)).filter((Post.is_public == True) & (Post.author_id == user_id)).order_by(
        Post.modified_date.desc()).all()
    return posts


def get_user_notes(cur_user_id):
    session = db_session.create_session()
    notes = session.query(Post).filter((Post.is_public == False) & (Post.author_id == cur_user_id)).order_by(
        Post.modified_date.desc()).all()
    return notes


def append_post(form, user_id: int):
    session = db_session.create_session()
    post = Post()
    post = post_add_data(post, form, user_id)
    session.add(post)
    session.commit()


def post_add_data(post: Post, form, user_id: int):
    post.topic = form.topic.data
    post.text = form.text.data
    post.is_public = form.is_public.data
    post.author_id = user_id
    return post


def delete_post(post_id: int):
    session = db_session.create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise PostError(msg="There is no such post")
    session.delete(post)
    session.commit()
