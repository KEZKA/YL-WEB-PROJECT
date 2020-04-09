from flask import jsonify
from flask_restful import reqparse, abort, Resource
from sanansaattaja.data import db_session
from sanansaattaja.data.models.user import User


def abort_if_user_not_found(user_id):
    db = db_session.create_session()
    user = db.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db = db_session.create_session()
        user = db.query(User).get(user_id)
        return jsonify({'news': user.to_dict(rules=('-hashed_password', '-news'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db = db_session.create_session()
        user = db.query(User).get(user_id)
        db.delete(user)
        db.commit()
        return jsonify({'success': 'ok'})


class UserListResource(Resource):
    def get(self):
        db = db_session.create_session()
        users = db.query(User).all()
        return jsonify({'users': [item.to_dict(
            rules=('-hashed_password', '-jobs', '-news')) for item in users]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('age', required=False, type=int)
        parser.add_argument('nickname', required=False)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        db = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            nickname=args['nickname'],
            email=args['email'],
        )
        user.set_password(args['password'])
        db.add(user)
        db.commit()
        return jsonify({'success': 'OK'})