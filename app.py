from flask import Flask, render_template, redirect # type: ignore

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    return render_template("logout.html", titolo="logout", header="logout")

@app.route("/register")
def register():
    return render_template("register.html", titolo="register", header="register")

@app.route("/login")
def login():
    return render_template("login.html", titolo="login", header="login")


@app.route("/personal")
def personal():
    ...

app.run(debug=True)
