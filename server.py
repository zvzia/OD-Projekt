from flask import Flask, render_template, request, make_response, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import markdown
from collections import deque
from passlib.hash import sha256_crypt
import sqlite3

from data_bese import *

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "206363ef77d567cc511df5098695d2b85058952afd5e2b1eecd5aed981805e60"

DATABASE = "./notes_app.db"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username is None:
        return None

    row = get_user_by_username(username)
    try:
        username, password = row
    except:
        return None

    user = User()
    user.id = username
    user.password = password
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = user_loader(username)
    return user


recent_users = deque(maxlen=3)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = user_loader(username)
        if user is None:
            return "Nieprawidłowy login lub hasło", 401
        if sha256_crypt.verify(password, user.password):
            login_user(user)
            return redirect('/start_page')
        else:
            return "Nieprawidłowy login lub hasło", 401

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/start_page", methods=['GET'])
@login_required
def hello():
    if request.method == 'GET':
        print(current_user.id)
        username = current_user.id

        notes = get_notes_id_by_username(username)

        return render_template("start_page.html", username=username, notes=notes)

@app.route("/render", methods=['POST'])
@login_required
def render():
    md = request.form.get("note","")
    rendered = markdown.markdown(md)
    username = current_user.id

    insert_note(username, rendered)

    return render_template("note.html", rendered=rendered)

@app.route("/render/<rendered_id>")
@login_required
def render_old(rendered_id):
    row = get_note_by_id(rendered_id)

    try:
        username, rendered = row
        if username != current_user.id:
            return "Access to note forbidden", 403
        return render_template("markdown.html", rendered=rendered)
    except:
        return "Note not found", 404

if __name__ == "__main__":
    print("[*] Init database!")
    create_user_table()
    create_notes_table()
    

    app.run("0.0.0.0", 5000)