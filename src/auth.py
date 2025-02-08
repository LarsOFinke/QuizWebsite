from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db.crud import add_login, validate_login, get_all_usernames


auth = Blueprint('auth', __name__)


@auth.route('/clear-session', methods=['GET'])
def clear_session():
    session.clear()  # Clear the session
    return redirect(url_for('auth.login'))


@auth.route('/', methods=['GET', 'POST'])
def login():
    if session.get("login_confirmed"):
        return redirect(url_for('views.selection'))
    
    if request.method == 'POST':
        action:str = request.form.get("login")
        
        match action:
            case "guest":
                session["login_confirmed"] = True
                session["username"] = "guest"
                return redirect(url_for('views.selection'))
        
            case "login":
                username: str = request.form.get('username')
                password: str = request.form.get('password')
                
                if validate_login(username, password):
                    session["login_confirmed"] = True
                    session["username"] = username

                    if session["username"] == "admin":
                        session["is_admin"] = True
                    else:
                        session["is_admin"] = False

                    return redirect(url_for('views.selection'))
            
                else:
                    flash("Ungültige Login-Daten!")
                    return redirect(url_for('auth.login'))
    
    return render_template('login.html')



@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        password2: str = request.form.get('password2')

        if password != password2:
            flash("Passwörter stimmen nicht überein!", "error")
        
        elif len(password) < 8:
            flash("Das Passwort muss mindestens 8 Zeichen lang sein!", "error")
            
        elif username in get_all_usernames():
            flash("Der Nutzername ist bereits vergeben!", "error")
        
        else:
            add_login(username, password)
            flash("Accounterstellung erfolgreich!", "info")
        
        return redirect(url_for('auth.register'))
    
    
    return render_template('register.html')