from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import markdown
from collections import deque
from passlib.hash import sha256_crypt
import bleach
from time import sleep
from datetime import datetime
from flask_simple_geoip import SimpleGeoIP
import threading
from flask_wtf.csrf import CSRFProtect

from data_bese import *
from services.device_services import *
from services.email_services import *
from services.services import *


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "206363ef77d567cc511df5098695d2b85058952afd5e2b1eecd5aed981805e60"

DATABASE = "./notes_app.db"

app.config.update(GEOIPIFY_API_KEY='at_B4q3tYTX5aD0zzGsa5gxpCeHvmHTz')
simple_geoip = SimpleGeoIP(app)

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
    user.username = username
    user.password = password
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = user_loader(username)
    return user


recent_users = deque(maxlen=3)

csrf = CSRFProtect()
csrf.init_app(app)

@app.route("/test")
def test():
    now = datetime.now()
    return 200


@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")
    if request.method == "POST":
        username = bleach.clean(request.form.get("username"))
        password = bleach.clean(request.form.get("password"))
        user = user_loader(username)
        ip = request.remote_addr
        location = get_location_info(ip, simple_geoip)
        device = get_device(request.headers.get('User-Agent'))

        if user is None:
            return "Nieprawidłowy login lub hasło", 401
        
        active = get_user_by_username(username)[4]
        if(active == 'false'):
            return "Thic account is deactivated, please check your mailbox", 200
        if sha256_crypt.verify(password, user.password):
            login_user(user)
            isNew = check_if_new_device(username, device, location)
            if isNew:
                th = threading.Thread(target=send_email_if_new_device, args=(username, device, location))
                th.start()
                return "Check your mailbox and confirm login", 200
            return redirect('/start_page')
        else:
            sleep(2)
            user_id = get_user_by_username(username)[0]
            insert_failed_login(user_id, str(datetime.now())[:-7], ip, location, device)
            th = threading.Thread(target=send_email_and_block_account_if_needed, args=(username, device, location))
            th.start()
            return "Nieprawidłowy login lub hasło", 401


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register_page.html")
    if request.method == "POST":
        sleep(1)
        username = bleach.clean(request.form.get("username"))
        password = bleach.clean(request.form.get("password"))
        password_retyped = bleach.clean(request.form.get("password_retyped"))
        email = bleach.clean(request.form.get("email"))

        ip = request.remote_addr
        location = get_location_info(ip, simple_geoip)
        device = get_device(request.headers.get('User-Agent'))
        
        if password == password_retyped:
            if not chceck_if_user_exist(username):
                password_encrypted = hash_password(password)
                insert_user(username, email, password_encrypted)
                user = user_loader(username)
                login_user(user)

                user_id = get_user_by_username(username)[0]
                insert_autorized_device(user_id, location, device)
                return redirect('/start_page')
            else:
                return "Taki użytkownik już istnieje", 401
        else:
            return "Hasła nie pokrywają sie", 401

@app.route("/changepasswordrequest", methods=["GET","POST"])
def changepasswordrequest():
    if request.method == "GET":
        return render_template("change_password.html")
    if request.method == "POST":
        username = bleach.clean(request.form.get("username"))
        user_info = get_user_by_username(username)
        if user_info != None:
            th = threading.Thread(target=send_email_with_password_change_link, args=(username,))
            th.start()
        return "Chceck your mailbox. <br> <a href=\"/\"><button>Go back</button></a>", 200

@app.route("/changepassword", methods=['POST'])
def changepassword():
    if request.method == "POST":
        user_id = bleach.clean(request.form.get("user_id"))
        password = bleach.clean(request.form.get("password"))
        password_retyped = bleach.clean(request.form.get("password_retyped"))
        token = bleach.clean(request.form.get("token"))
        
        token_info = get_token_info(token)
        if token_info == None:
            return "Invalid request", 404
        if token_info[0] != user_id:
            return "Invalid request", 404


        username = get_username_by_id(user_id)
        
        if password == password_retyped:
            if not chceck_if_user_exist(username):
                return "Taki użytkownik nie istnieje", 401
            else:
                password_encrypted = hash_password(password)
                change_password_by_username(username, password_encrypted)
                delete_token_from_db(token)
                activate_account_by_username(username)
                return "Password has been changed", 200
        else:
            return "Hasła nie pokrywają sie", 401

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/start_page", methods=['GET'])
@login_required
def start():
    if request.method == 'GET':
        username = current_user.username

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
    allowed_tags = ['p', 'b', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'a', 'img', 'strong', 'em']
    allowed_atributes = {
        'a': ['href'],
        'img' : ['src', 'width', 'height']
    }
    md = bleach.clean(request.form.get("markdown",""), tags=allowed_tags, attributes=allowed_atributes)
    rendered = markdown.markdown(md)
    username = current_user.username
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

        if username != current_user.username:
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

        if to_user != current_user.username:
            return "Access to note forbidden", 403
        return render_template("note.html", rendered=rendered, noteid=rendered_id, shared=True)
    except:
        return "Note not found", 404


@app.route("/share/<note_id>", methods=["GET","POST"])
@login_required
def share(note_id):
    if request.method == 'GET':
        return render_template("share_note.html", noteid=note_id)
    if request.method == 'POST':
        shared_to = bleach.clean(request.form.get("shareto"))
        shared_by = current_user.username
        note_record = get_note_by_id(note_id)
        rendered = note_record[2]
        encrypted = note_record[1]
        title = note_record[4]

        if(encrypted == 'true'):
            return "You cant share this note", 403
        
        if(note_record[0] != current_user.username):
            return "Access to note forbidden", 403

        shared_to_id = get_user_by_username(shared_to)[0]
        shared_by_id = get_user_by_username(shared_by)[0]

        insert_shared_note(shared_by_id, shared_to_id, note_id, title)
        
        return render_template("note.html", rendered=rendered, noteid=note_id)


@app.route("/public_share/<note_id>", methods=['GET'])
@login_required
def public_share(note_id):
    if request.method == 'GET':
        note_info = get_note_by_id(note_id)
        encrypted = note_info[1]
        if(encrypted == 'true'):
            return "You cant share this note", 403

        owner = note_info[0]
        if(owner != current_user.username):
            return "Access to note forbidden", 403

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

        note_info = get_note_by_id(note_id)
        owner = note_info[0]
        rendered = note_info[2]

        decrypted = decrypt_note(rendered, password)

        if owner != current_user.username:
            return "Access to note forbidden", 403

        return render_template("note.html", rendered=decrypted, encrypted="true", noteid=note_id)

        

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    note_id = bleach.clean(request.form.get("note_id"))
    note_record = get_note_by_id(note_id)

    owner = note_record[0]
    if owner != current_user.username:
        return "Action forbidden", 403
        
    delete_note_by_id(note_id)
    return redirect(url_for('start'))


@app.route("/securityaction", methods=['GET'])
def securityaction():
    if request.method == 'GET':
        action  = request.args.get('action', None)
        token  = request.args.get('token', None)

        token_info = get_token_info(token)
        if(token_info == None):
            return "Invalid request", 404

        user_id = token_info[0]
        token_action = token_info[1]
            
        if(token_action != action):
            return "Invalid request", 404

        if(action == "changepassword"):
            return render_template("change_password_form.html", userid=user_id, token=token)

        elif(action == "confirmlogin"):
            location  = request.args.get('location', None)
            device  = request.args.get('device', None)
            insert_autorized_device(user_id, location, device)
            delete_token_from_db(token)
            return "You confirmed login", 200
        elif(action == "activateaccount"):
            return render_template("change_password_form.html", userid=user_id, token=token)
        else:
            return "Invalid request", 404


if __name__ == "__main__":
    print("[*] Init database!")
    create_user_table()
    create_notes_table()
    create_sharedNotes_table()
    create_failed_login_table()
    create_autorized_device_table()
    create_token_table()

    #app.run(ssl_context='adhoc')     
    app.run("0.0.0.0", 5000)