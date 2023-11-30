import math
from flask import render_template, request, redirect, jsonify
from flask import session as login_session
from dao import *
from App import app, login, db
from App import admin
from App.models import User, Message, Blog
from flask_login import login_user, current_user, UserMixin, AnonymousUserMixin
from stego import *

k = app.config["KEY"]


def display_content(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()
        file_content = " ".join(file_content)
        file.close()

    return file_content


def content_list(blog):
    return display_content(blog[0].content)


def download_blog(title, message, em_text, user_id):
    print("Start downloading!")
    # print((get_last_message_id()))
    m = Message(k=k, message=message, user_id=user_id)
    db.session.add(m)
    db.session.commit()

    path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\\" + title + ".txt"
    file = open(path, "w")
    file.write(em_text)
    file.close()

    b = Blog(title=title,
             content=path,
             user_id=user_id, message_id=int(get_last_message_id()))
    db.session.add(b)
    db.session.commit()
    print("Finish downloading!")


@app.route("/")
def home():
    blogs = get_all_blogs()

    num = count_blogs()
    page_size = app.config["PAGE_SIZE"]
    return render_template("index.html", blogs=blogs, contents=content_list(blogs),
                           pages=math.ceil(num/page_size), current_user=current_user)


@app.route('/activate_function', methods=['POST'])
def activate_function():

    data = request.get_json()
    param1 = data.get('title')
    param2 = data.get('message')
    param3 = data.get('em_text')
    param4 = data.get('user_id')

    #print(param4)
    download_blog(param1, param2, param3, param4)
    return jsonify({'message': 'Function activated with parameters!'})


@app.route("/decode")
def decode():
    content = request.args.get("de_cover_text_content")

    if not content:
        blog_id = request.args.get("blog")
        if not blog_id:
            content = ""
        else:
            content = content_list(get_blog(blog_id))

    content = adjust_enter(content)
    k = app.config["KEY"]

    msg = ""
    if content:
        msg = giai_thong_diep(giai_ma_nhi_phan(content, key=app.config["KEY"]))

    return render_template("decode.html",
                           content=content, message=msg)


@app.route("/encode")
def encode():
    k = app.config["KEY"]

    title = request.args.get("en_cover_text_title")
    if not title:
        title = ""

    content = request.args.get("en_cover_text_content")
    if not content:
        content = ""
    else:
        content = adjust_enter(content)

    msg = request.args.get("en_msg")
    if not msg:
        msg = ""

    em_text = ""

    if title != "" and content != "" and msg != "":
        if not dieu_kien(content, msg, k):
            em_text = "Văn bản chứa không đủ lớn để chứa thông tin mật"
        else:
            em_text = nhung(ma_hoa_thong_diep(msg), tach_chuoi(content, k))

    return render_template("encode.html", title=title,
                           content=content, msg=msg, em_text=em_text)


@login.user_loader
def load_user(user_id):
    # print(db.session.query(User).get(user_id))
    # print("message:", User.query.get(user_id))
    return db.session.get(User, user_id)


@app.route("/admin/login", methods=["post"])
def login_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    user = auth_user(username=username, password=password)

    if user:
        login_user(user)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)

    r"""content = display_content(r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Mastering Your Time Proven Strategies for Boosting Productivity.txt")
    k = app.config["KEY"]
    msg = "Found a teddy bear"
    #em_text = nhung(chuoi_nhi_phan=ma_hoa_thong_diep("Found a teddy bear"), chuoi_con=tach_chuoi(content, k))
    old_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Mastering Your Time Proven Strategies for Boosting Productivity - Copy.txt"
    new_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Mastering Your Time Proven Strategies for Boosting Productivity.txt"
    content = display_content(old_path)
    content = adjust_enter(content)
    #print(tach_chuoi(content, k))
    em_text = nhung(chuoi_nhi_phan=ma_hoa_thong_diep("Found a teddy bear"), chuoi_con=tach_chuoi(content, k))

    # with open(new_path) as file:
    file = open(new_path, "w")
    file.write(em_text)
    file.close()

    file = open(new_path, "r")
    content = file.read()
    print(content)

    de_text = display_content(new_path)
    de_text = adjust_enter(de_text)
    print(giai_thong_diep(giai_ma_nhi_phan(de_text, k)))
    title = "hello world"
    em_text = "konbanwa"
    path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\\" + title + ".txt"
    file = open(path, "w")
    file.write(em_text)
    file.close()"""


