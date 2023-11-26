import math
from flask import render_template, request, redirect
import dao
from App import app, login
from App import admin
from App.models import User
from flask_login import login_user, current_user, UserMixin, AnonymousUserMixin
from stego import *


def display_content(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()
        file_content = " ".join(file_content)
        file.close()

    return file_content


def content_list(blog):
    return display_content(blog[0].content)


@app.route("/")
def home():
    blogs = dao.get_all_blogs()

    num = dao.count_blogs()
    page_size = app.config["PAGE_SIZE"]
    return render_template("index.html", blogs=blogs, contents=content_list(blogs),
                           pages=math.ceil(num/page_size), current_user=current_user)


@app.route("/decode")
def decode():
    blog_id = request.args.get("blog")
    content = content_list(dao.get_blog(blog_id))
    content = content.strip()
    k = app.config["KEY"]
    msg = nhung(chuoi_nhi_phan=ma_hoa_thong_diep("Found a teddy bear"), chuoi_con=tach_chuoi(content, k))
    #msg=(giai_ma_nhi_phan(content, key=app.config["KEY"]))
    #100011110001100000010000000010111000011010010000111111001000100100000
    #000011110001100000011110000101110000110100100100000010100010010000011101000011100000110100001101001000100010010000001011000011100000101000011011
    return render_template("decode.html",
                           content=content, message=msg)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/admin/login", methods=["post"])
def login_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)

    r"""content = display_content(r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Mastering Your Time Proven Strategies for Boosting Productivity.txt")
    k = app.config["KEY"]
    # print(tach_chuoi(content, k))
    #em_text = nhung(chuoi_nhi_phan=ma_hoa_thong_diep("Found a teddy bear"), chuoi_con=tach_chuoi(content, k))
    #print(tach_chuoi(em_text, k))
    #print(em_text)
    content = content.strip()
    #print(content)
    #print(ma_hoa_thong_diep("Found a teddy bear"))
    print("message:", tach_chuoi(content, k))
    #print("Introduction:\n In a")"""


