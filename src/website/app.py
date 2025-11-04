# website/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from db.db import init_db, add_user, check_user  

app = Flask(__name__)
app.secret_key = "placeholder" # not set yet   

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    
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
        clicked_button = request.form.get("action")  

        print(username,"<u", password , "<p")

        if not  username or not password:
            if clicked_button == "Login" or clicked_button == "Register":
                flash("Username and password cannot be empty!", "warning")
            return render_template("register.html", greeting=greeting)

        if clicked_button == "Register":
            success, message = add_user(username, password)
            if success:
                session["username"]=username 
                return redirect(url_for("api"))
            else:
                if clicked_button == "Login" or clicked_button == "Register":
                    flash(message, "error")
        elif clicked_button == "Login":
            if check_user(username, password):
                session["username"]=username 
                return redirect(url_for("api"))
            else:
                if clicked_button == "Login" or clicked_button == "Register":
                    flash("Invalid username or password","error")

    return render_template("register.html", greeting=greeting)

@app.route("/api",methods = ["POST","GET"])

def api():
    
    # api 
    
    clicked_button = None

    if request.method == "POST":
        clicked_button = request.form.get("action")
    
    if clicked_button == "Logout":
        print('yes')
        session["username"] = None
        return redirect(url_for("register"))

    greeting = "Welcome Back, " + session["username"]
    return render_template("home.html",greeting = greeting)
    
