from App import models
from App.models import Message, Blog, User
from App import app, db
import hashlib


def get_all_blogs():
    return Blog.query.all()


def get_blog(blog_id):
    return Blog.query.filter(Blog.id.contains(blog_id))


def get_last_message_id():
    return Message.query.order_by(Message.id.desc()).first()


def count_blogs():
    return Blog.query.count()


def get_user(user_id):
    return User.get.query(user_id)


def get_user_by_name(name):
    return User.query.filter(User.username.contains(name)).first()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()
