from flask import Flask, render_template #, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/signin", methods = ["GET", "POST"])
# def signIn():
#     name = request.form["name"]
#     member_id = request.form["member_id"]
#     # print(f"{name} {member_id}")
#     return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/items")
def items():
    return {"Diamond": 1000, "Sphinx": 400}

if __name__ == "__main__":
    app.run(debug=True)