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

@app.route("/homepage")
def index():
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def check():
    session.clear()
    username=request.form.get("username")
    password=str(request.form.get("password"))
    h = hashlib.md5(password.encode())
    password=h.hexdigest()
    exsitusers=list(db.execute("SELECT username,password FROM users").fetchall())
  
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
        return render_template("register.html")
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

@app.route("/signout")
def signout():
    session.clear()
    return render_template("index.html")

@app.route("/categories", methods=["GET", "POST"])
def categories():
   # names = request.form.get("category")
    names=request.form.getlist("category")
    print(names)
    business=[['Atla', '372 Lafayette St', 'Daniela Soto-Innes', 'https://www.atlanyc.com/', 'Food-and-Drink', 'atla.jpg'], ['Atoboy and Atomix', '43 E. 28th St, New York, NY', 'Ellia Park', 'https://www.atomixnyc.com/ ', 'Food-and-Drink' , 'AtoboyandAtomix.jpg']] 
    business+=[['Ayada', '7708 Woodside Ave, New York, NY', 'Duanjai Thammasat', 'https://ayadathai.com/', 'Food-and-Drink', 'Ayada.jpeg'], ['Baoburg', '614 Manhattan Ave Brooklyn', 'Suchanan Aksornnan', 'http://www.baoburg.com/ ', 'Food-and-Drink', 'Baoburg.jpg'], ['CAP Beauty', '238 West 10 St, New York"', 'Chloe Kernaghan', 'https://www.capbeauty.com/', 'Hair-and-Beauty', 'CAPBeauty.jpg'], ['The Sill', '84 Hester Street, New York, NY', 'Eliza Blank', 'https://www.thesill.com/ ', 'Home Décor', 'TheSill.jpg'], ['McNally Jackson', '52 Prince St, New York, NY', 'Sarah McNally', 'https://www.mcnallyjackson.com/', 'Books', 'McNallyJackson.jpg'], ['Frankie', '100 Stanton St , New York, NY', 'Gaelle Drevet', 'https://thefrankieshop.com/', ('Retail','Home Décor'), 'Frankie.jpg'], ['Maryam Nassir Zadeh', '123 Norfolk St, New York, NY', 'Maryam Nassir Zadeh', 'https://mnzstore.com/', 'Retail', 'MaryamNassirZadeh.jpg']]
    if len(names)==0:
        return render_template("homepage.html", business= business)
    else:
        z=[]
        for x in range(0,len(names)):
            for i in business:
                print(z)
                print(x)
                if names[x] in i[4]:
                    z+=[i]
                    
        print(z)
        return render_template("homepage.html",business= z)       

@app.route("/temp")
def temp():
    return render_template('review.html')
@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == 'POST':
        customer = request.form.get('username')
        company = request.form.get('company')
        rating = request.form.get('rating')
        review = request.form.get('comments')

        if customer == '' or company == '' or review== '':
            return render_template('review.html', message='Please enter required fields')
        else:
            db.execute("INSERT INTO reviews username, company, review, rating) VALUES (:username, :company, :review, :rating)",
              {"username": customer, "company": company, "review": review, "rating": rating})
            db.commit()
    exsitreviews=list(db.execute("SELECT username, company, review, rating FROM reviews").fetchall())
    allreviews=[]
    for i in exsitreviews:
        allreviews+=[list(i)]
    print(allreviews)
    return render_template('review.html', review=allreviews)