import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import hashlib


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def check():
    session.clear()
    username=request.form.get("username")
    password=str(request.form.get("password"))
    h = hashlib.md5(password.encode())
    password=h.hexdigest()
    exsitusers=list(db.execute("SELECT username,password FROM users").fetchall())
    print(username,password)
  
    if (username,password) in exsitusers:
             return render_template("homepage.html")
    if username!=None:
        alert="Wrong Username or Password. Please try again."
        return render_template("index.html", alert=alert)
    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    username=request.form.get("username")
    password=str(request.form.get("password"))
    if len(password)<=6:
        alert='Password must be six characters. Please try another password.'
        return render_template("register.html",alert=alert)
    exsitusers=list(db.execute("SELECT username FROM users").fetchall())
    lenU=len(exsitusers)
    h = hashlib.md5(password.encode())
    password=h.hexdigest()
    alert="This username already exists please choose another one!"
    if username!=None and password!=None:
        if lenU>0:
            for i in exsitusers:
                if username in i[0]:
                    return render_template("register.html",alert=alert)
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
              {"username": username, "password": password})
        db.commit()
        return render_template("homepage.html")
    return render_template("register.html")
