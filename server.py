from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import markdown
from collections import deque
from passlib.hash import sha256_crypt
import bleach

from data_bese import *
from services import *

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
        username = row[1]
        password = row[3]
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
        username = bleach.clean(request.form.get("username"))
        password = bleach.clean(request.form.get("password"))
        user = user_loader(username)
        if user is None:
            return "Nieprawidłowy login lub hasło", 401
        if sha256_crypt.verify(password, user.password):
            login_user(user)
            return redirect('/start_page')
        else:
            return "Nieprawidłowy login lub hasło", 401


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register_page.html")
    if request.method == "POST":
        username = bleach.clean(request.form.get("username"))
        password = bleach.clean(request.form.get("password"))
        password_retyped = bleach.clean(request.form.get("password_retyped"))
        email = bleach.clean(request.form.get("email"))
        
        if password == password_retyped:
            if not chceck_if_user_exist(username):
                password_encrypted = hash_password(password)
                insert_user(username, email, password_encrypted)

                user = user_loader(username)
                login_user(user)
                return redirect('/start_page')
            else:
                return "Taki użytkownik już istnieje", 401
        else:
            return "Hasła nie pokrywają sie", 401

@app.route("/changepassword", methods=["GET","POST"])
def changepassword():
    if request.method == "GET":
        return render_template("change_password.html")
    if request.method == "POST":
        username = bleach.clean(request.form.get("username"))
        user_info = get_user_by_username(username)
        if user_info != None:
            send_email_with_password_change_link(username)
        
        return "Chceck your mailbox. <br> <a href=\"/\"><button>Go back</button></a>", 200


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/start_page", methods=['GET'])
@login_required
def start():
    if request.method == 'GET':
        print(current_user.id)
        username = current_user.id

        notes = get_notes_id_by_username(username)
        shared_notes = get_shared_notes_id_by_username(username)

        return render_template("start_page.html", username=username, notes=notes, shared_notes=shared_notes)

@app.route("/add_note", methods=['GET'])
@login_required
def add_note():
    if request.method == 'GET':
        return render_template("add_note.html")

@app.route("/render", methods=['POST'])
@login_required
def render():
    allowed_tags = ['p', 'b', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'a', 'img']
    allowed_atributes = {
        'a': ['href'],
        'img' : ['src', 'width', 'height']
    }
    md = bleach.clean(request.form.get("markdown",""), tags=allowed_tags, attributes=allowed_atributes)
    rendered = markdown.markdown(md)
    username = current_user.id
    encrypt = request.form.get("encrypt")
    title = bleach.clean(request.form.get("title"))

    if encrypt == "encrypt":
        password = bleach.clean(request.form.get("password"))
        password_retyped = bleach.clean(request.form.get("password_retyped"))
        if password == password_retyped:
            encrypted = encrypt_note(rendered, password)
            insert_note(username, encrypted, "true", title, "false")
        else:
            return "Hasła nie pokrywają sie", 401
    else:
        insert_note(username, rendered, "false", title, "false")
        
    return render_template("rendered.html", rendered=rendered)

@app.route("/render/<rendered_id>")
@login_required
def render_old(rendered_id):
    row = get_note_by_id(rendered_id)

    try:
        username = row[0]
        encrypted = row[1]
        rendered = row[2]

        if username != current_user.id:
            return "Access to note forbidden", 403
        if encrypted == "true":
            return redirect('/decrypt/' + str(rendered_id))
        return render_template("note.html", rendered=rendered, encrypted=encrypted, noteid=rendered_id)
    except:
        return "Note not found", 404

@app.route("/shared/<rendered_id>")
@login_required
def shared(rendered_id):
    note = get_note_by_id(rendered_id)
    info = get_shared_note_info_by_noteid(rendered_id)

    try:
        rendered = note[2]
        to_user_id = info[1]
        to_user = get_username_by_id(to_user_id)

        if to_user != current_user.id:
            return "Access to note forbidden", 403
        return render_template("note.html", rendered=rendered, noteid=rendered_id)
    except:
        return "Note not found", 404


@app.route("/share/<note_id>", methods=['GET'])
@login_required
def share(note_id):
    if request.method == 'GET':
        return render_template("share_note.html", noteid=note_id)


@app.route("/share", methods=['POST'])
@login_required
def share_post():
    note_id = bleach.clean(request.form.get("note_id"))
    shared_to = bleach.clean(request.form.get("shareto"))
    shared_by = current_user.id
    rendered = get_note_by_id(note_id)[2]

    shared_to_id = get_user_by_username(shared_to)[0]
    shared_by_id = get_user_by_username(shared_by)[0]

    insert_shared_note(shared_by_id, shared_to_id, note_id)
    
    return render_template("note.html", rendered=rendered, noteid=note_id)

@app.route("/public_share/<note_id>", methods=['GET'])
@login_required
def public_share(note_id):
    if request.method == 'GET':
        make_note_public(note_id)
        link = "http://127.0.0.1:5000/public_note/" + str(note_id)
        return "Link to your public note:<br>" + link + "<br> <a href=\"/start_page\"><button>Go back</button></a>", 200

@app.route("/public_note/<rendered_id>")
def render_public(rendered_id):
    row = get_note_by_id(rendered_id)
    public = row[3]

    if public == "false":
        return "Access to note forbidden", 403

    try:
        encrypted = row[1]
        rendered = row[2]

        return render_template("note.html", rendered=rendered, encrypted=encrypted, noteid=rendered_id)
    except:
        return "Note not found", 404


@app.route("/decrypt/<note_id>", methods=["GET","POST"])
def decrypt(note_id):
    if request.method == "GET":
        return render_template("note_decrypt.html", noteid = note_id)
    if request.method == "POST":
        password = bleach.clean(request.form.get("password"))

        row = get_note_by_id(note_id)
        username = row[0]
        rendered = row[2]

        decrypted = decrypt_note(rendered, password)

        if username != current_user.id:
            return "Access to note forbidden", 403
        return render_template("note.html", rendered=decrypted, encrypted="true", noteid=note_id)

        

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    note_id = bleach.clean(request.form.get("note_id"))
    delete_note_by_id(note_id)
    return redirect(url_for('start'))





if __name__ == "__main__":
    print("[*] Init database!")
    create_user_table()
    create_notes_table()
    create_sharedNotes_table()

    app.run("0.0.0.0", 5000)