from ccc_auction import app
from flask import render_template

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/") #, methods = ["GET", "POST"])
def signIn():
    # name = request.form["name"]
    # member_id = request.form["member_id"]
    # print(f"{name} {member_id}")
    return render_template("signin.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/items")
def items():
    return render_template("items.html")