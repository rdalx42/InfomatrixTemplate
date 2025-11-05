# website/app.py

from flask import Flask, render_template, request,redirect,url_for,flash, session
from datetime import datetime, timedelta
from db.db import init_db, add_user, get_user
from werkzeug.security import generate_password_hash,check_password_hash
from passlib.hash import sha256_crypt
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.permanent_session_lifetime = timedelta(days=30)

init_db()

@app.route("/",methods = ["GET"])

def home():
    return redirect(url_for("register"))

@app.route("/register",methods = ["GET","POST"])
def register():
    # auto redirect if user doesn't exist
    if "username" in session and session.get("remember_me"):
        if "already_quened" not in session:
            session["already_quened"] = False
        return redirect(url_for("api"))

    
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember")
        clicked_button = request.form.get("action")

        if not username or not password:
            flash("Username and password cannot be empty!", "warning")
            return render_template("register.html", greeting=greeting)

        # REGISTER new user
        if clicked_button == "Register":
            hashed_password = generate_password_hash(password)
            success, message = add_user(username, hashed_password)
            if success:
                session["username"] = username
                session["already_quened"] = False
                session.permanent = True  # optional for newly registered
                session["remember_me"] = bool(remember == "on")
                return redirect(url_for("api"))
            else:
                flash(message, "error")

        # LOGIN existing user
        elif clicked_button == "Login":
            user = get_user(username)
            if user and sha256_crypt.verify(password, user["password"]):
                session["username"] = username
                session["already_quened"] = False

                if remember == "on":
                    session.permanent = True
                    session["remember_me"] = True
                else:
                    session.permanent = False
                    session["remember_me"] = False

                return redirect(url_for("api"))
            else:
                flash("Invalid username or password", "error")

    return render_template("register.html", greeting=greeting)


@app.route("/api", methods=["GET", "POST"])

def api():
    
    # API INTEGRATION
    
    clicked_button = None
    if request.method == "POST":
        clicked_button = request.form.get("action")

    
    if clicked_button == "Logout":
        session.clear()
        return redirect(url_for("register"))

    
    if clicked_button == "Create" and not session.get("already_quened", False):
        session["already_quened"] = True

    username = session.get("username", "Guest")
    greeting = f"Welcome, {username} 👋"
    return render_template("home.html", greeting=greeting)
