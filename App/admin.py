from App.models import Blog, User, Message, UserRole
from App import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app, name="Quản trị bài blog", template_mode="bootstrap4")


class AuthenticateAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticateUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyBlogView(AuthenticateAdmin):
    column_list = ["id", "title", "content", "user_id", "message_id", "byte_key"]
    column_filters = ["title", "content"]
    column_searchable_list = ["title"]
    column_editable_list = ["title", "content"]
    edit_modal = True


class LogoutView(AuthenticateUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/")


admin.add_view(MyBlogView(Blog, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
