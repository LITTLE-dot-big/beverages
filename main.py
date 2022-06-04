from flask import Flask, render_template, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as r:
    parameters = json.load(r)['parameters']
local_server = parameters['local_server']

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    # MAIL_USERNAME=parameters['gmail_username'],
    # MAIL_PASSWORD=parameters['gmail_password']
)
mail = Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['local_uri']
# db = SQLAlchemy(app)


# class Contact(db.Model):
#     """name email phone message date"""
#     sno = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=False, nullable=False)
#     email = db.Column(db.String(50), unique=False, nullable=False)
#     phone = db.Column(db.String(15), unique=False, nullable=False)
#     message = db.Column(db.String(500), unique=False, nullable=True)
#     date = db.Column(db.String(15), unique=True, nullable=False)


@app.route("/")
def home():
    return render_template("index.html", params=parameters)


@app.route("/index")
def index():
    return render_template("index.html", params=parameters)


@app.route("/about/")
def about():
    return render_template("about.html", params=parameters)


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":  # Add entry to the database
        n = request.form.get("name")
        e = request.form.get("email")
        p = request.form.get("phone")
        m = request.form.get("message")
        # entry = Contact(name=n, email=e, phone=p, message=m, date=datetime.now())
        # db.session.add(entry)
        # db.session.commit()
        mail.send_message(
            f"New message from {n}, through {parameters['blog_name']}",
            sender=e,
            recipients=[parameters['gmail_username'],
                        parameters['gmail_Shubham']],
            body=f"{m}\nContact: {p}"
        )
    return render_template("contact.html", params=parameters)


@app.route("/products/", methods=["GET"])
def products():
    return render_template("products.html", params=parameters)


app.run(debug=True)
