from sanansaattaja.core.errors import UserError
from sanansaattaja.db.data import db_session
from sanansaattaja.db.data.models import User

MAX_FILE_SIZE = 1024 ** 2


def add_user(form, request):
	db = db_session.create_session()
	if form.password.data != form.password_again.data:
		raise UserError(msg="Passwords do not match")

	if db.query(User).filter(User.email == form.email.data).first():
		raise UserError(msg="This email is already in use")

	if request.files['photo']:
		filename = request.files['photo'].filename
		if filename.split('.')[-1].lower() not in ('jpg', 'png', 'gif'):
			raise UserError(msg="Invalid extension of image")
		file = request.files['photo'].read(MAX_FILE_SIZE)
		if len(file) == MAX_FILE_SIZE:
			return UserError(msg="File size is too large")
	else:
		file = None
	user = User()
	print(form.name.data)
	user.name = form.name.data,
	user.surname = form.surname.data,
	user.email = form.email.data,
	user.age = form.age.data,
	user.sex = form.sex.data,
	user.profile_picture = file
	user.set_password(form.password.data)
	db.add(user)
	db.commit()