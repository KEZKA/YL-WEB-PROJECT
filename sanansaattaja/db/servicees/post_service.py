from sqlalchemy import not_, func
from sqlalchemy.orm import selectinload

from sanansaattaja.core.errors import ClientError, IdError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import Post
from sanansaattaja.db.servicees.comment_service import delete_all_comment
from sanansaattaja.website.forms import PostSearchForm


def get_all_public_posts():
    session = db_session.create_session()
    posts = session.query(Post).options(selectinload(Post.author)).filter(Post.is_public).order_by(
        Post.modified_date.desc()).all()
    session.close()
    return posts


def get_all_user_posts(user_id):
    session = db_session.create_session()
    posts = session.query(Post).options(selectinload(Post.author)).filter(
        Post.is_public & (Post.author_id == user_id)).order_by(
        Post.modified_date.desc()).all()
    session.close()
    return posts


def get_post_by_id(post_id):
    session = db_session.create_session()
    post = session.query(Post).options(selectinload(Post.author)).get(post_id)
    session.close()
    return post


def get_user_notes(cur_user_id):
    session = db_session.create_session()
    notes = session.query(Post).options(selectinload(Post.author)).filter(
        not_(Post.is_public) & (Post.author_id == cur_user_id)).order_by(
        Post.modified_date.desc()).all()
    session.close()
    return notes


def append_post(form, user_id: int):
    session = db_session.create_session()
    try:
        post = Post()
        post = post_add_data(post, form, user_id)
        session.add(post)
        session.commit()
    except Exception:
        raise ClientError(msg='failed to add a post')
    session.close()


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
        raise IdError(msg="There is no such post")
    delete_all_comment('post', post.id)
    session.delete(post)
    session.commit()
    session.close()


def search_posts(form: PostSearchForm):
    session = db_session.create_session()
    text = "%" + form.text.data + "%"
    posts = session.query(Post).options(selectinload(Post.author)).filter(Post.is_public, (Post.topic.like(text) | Post.text.like(text))).order_by(
    Post.modified_date.desc()).all()
    return posts
