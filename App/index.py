import math
from flask import render_template, request, redirect, jsonify
from flask import session as login_session
from dao import *
from App import app, login, db
from App import admin
from App.models import User, Message, Blog
from flask_login import login_user, current_user, UserMixin, AnonymousUserMixin
from stego import *
from AES import *
import pyAesCrypt


k = app.config["KEY"]
k_ase = app.config["KEY_ASE"]


def display_content_rb(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        #file_content = " ".join(file_content)
        return file_content


def display_content(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()
        file_content = " ".join(file_content)

    return file_content


def content_list(blog):
    return display_content(blog[0].content)


def content_list_rb(blog):
    return display_content_rb(blog[0].content)


def is_text_file(file_path, chunk_size=1024):
    with open(file_path, 'rb') as file:
        content = file.read(chunk_size)
        while content:
            if b'\x00' in content:
                return False  # Null bytes found, likely binary
            content = file.read(chunk_size)
    return True  # No null bytes found, likely text


def download_blog(title, message, em_text, user_id):
    # print("Start downloading!")
    m = Message(k=k, message=message, user_id=user_id)
    db.session.add(m)
    db.session.commit()

    em_text = encrypt_file(em_text, k_ase)

    path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\\" + title + ".txt"
    file = open(path, "wb")
    file.write(em_text)
    file.close()

    b = Blog(title=title,
             content=path, byte_key=k_ase,
             user_id=user_id, message_id=get_last_message_id().id)
    db.session.add(b)
    db.session.commit()
    # print("Finish downloading!")


@app.route("/")
def home():
    #blogs = get_all_blogs()
    #num = count_blogs()
    #page_size = app.config["PAGE_SIZE"]
    kw = request.args.get("kw")
    blogs = get_blog_kw(kw)

    return render_template("index.html", blogs=blogs
                           #pages=math.ceil(num/page_size)
                            , current_user=current_user)


@app.route("/content")
def content():
    blog_id = request.args.get('blog')
    blog = get_blog(blog_id)

    if not is_text_file(blog[0].content):
        contents = content_list_rb(get_blog(blog_id))
        contents = decrypt_file(contents, get_blog(blog_id)[0].byte_key)
    else:
        contents = content_list(get_blog(blog_id))

    return render_template("content.html", blog=blog, content=contents)


@app.route('/activate_function', methods=['POST'])
def activate_function():
    #print("Hello")
    data = request.get_json()
    #print('Received data:', data)
    param1 = data.get('title')
    param2 = data.get('message')
    param3 = data.get('em_text')
    param4 = data.get('user_id')

    # print(data)
    #print("Hello", param4)
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
            if is_text_file(get_blog(blog_id)[0].content):
                content = content_list(get_blog(blog_id))
            else:
                content = content_list_rb(get_blog(blog_id))
                content = decrypt_file(content, get_blog(blog_id)[0].byte_key)

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
    return db.session.get(User, user_id)


@app.route("/admin/login", methods=["post"])
def login_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    user = auth_user(username=username, password=password)

    if user:
        login_user(user)
        if username != "admin":
            return redirect("/")
        else:
            return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)

    r"""# with open(new_path) as file:
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
    file = open(path, "x")
    file.write(em_text)
    file.close()
    key = app.config["KEY_ASE"]
    print(key)
    text = "hello world\nI'm ken\nHow are you"
    cipher = encrypt_file_2(text, key)
    print(cipher)
    plaintext = decrypt_file_2(cipher, key)
    print(plaintext)
    # print(type((k_ase).encode("utf-8")))
    with app.app_context():
        print(get_blog(1)[0].byte_key)

    new_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Exploring the Wonders of Artificial Intelligence.txt"
    file = open(new_path, "r")
    content = file.read()
    em_text = encrypt_file(content, k_ase)

    file = open(new_path, "wb")
    file.write(em_text)

    file = open(new_path, "rb")
    content = file.read()
    content = decrypt_file(content, k_ase)
    print(content)
    file.close()
    with app.app_context():
        new_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Exploring the Wonders of Artificial Intelligence.txt"
        file = open(new_path, "rb")
        content = file.read()
        content = decrypt_file(content, get_blog(4)[0].byte_key)
        file.close()
        print(content)
    with app.app_context():
        #print(get_blog(4)[0].byte_key)
        new_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Exploring the Wonders of Artificial Intelligence.txt"
        file = open(new_path, "r")
        content = file.read()
        em_text = encrypt_file(content, get_blog(4)[0].byte_key)

        file = open(new_path, "wb")
        file.write(em_text)
        new_path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\Exploring the Wonders of Artificial Intelligence.txt"
        file = open(new_path, "rb")
        content = file.read()
        content = decrypt_file(content, get_blog(4)[0].byte_key)
        file.close()
        print(content)"""
    #em_text = encrypt_file(em_text, k_ase)
    #path = r"C:\Users\Khanh\Desktop\Text-Stegaography\App\blogs\\" + title + ".txt"

