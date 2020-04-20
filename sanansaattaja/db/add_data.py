from sanansaattaja.db.data.models import User
from sanansaattaja.db.data import db_session

db_session.global_init("sanansaattaja.db")
db = db_session.create_session()

user = User()
user.surname = "Scott"
user.name = "Ridley"
user.age = 21
user.email = "scott_chief@mars.org"
user.set_password('password')

user1 = User()
user1.surname = "Scott 1"
user1.name = "Ridley"
user1.age = 23
user1.email = "scott1_bad_colonist@mars.org"
user.set_password('password')

user2 = User()
user2.surname = "Scott 2"
user2.name = "Ridley"
user2.age = 24
user2.email = "scott2_mega_colonist@mars.org"
user.set_password('password3')

db.add(user)
db.add(user1)
db.add(user2)

user = User()
user.surname = "Chemer"
user.name = "Sophia"
user.age = 16
user.email = "world.is.unpredictable@gmail.com"
user.set_password('1234567')

db.add(user)


db.commit()
