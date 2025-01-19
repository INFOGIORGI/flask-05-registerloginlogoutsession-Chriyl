from flask import Flask, render_template, redirect, request, url_for, flash # type: ignore
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *


app = Flask(__name__)
app.secret_key = "AlbertoCorvaglia1234567890"
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
app.config["MYSQL_DB"] = "w3schools"
                        
Mysql= MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo="home", header="home")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        return render_template("logout.html", titolo="logout", header="logout")
    elif request.method == "POST":
        nome: str = request.form.get("nome", "")
        username: str = request.form.get("username", "")
        password: str = request.form.get("pswd", "")

        if isEmpty([nome, username, password]):
            flash("non ci possono essere campi vuoti")
            return redirect(url_for("login"))
        try:
            cursor = Mysql.connection.cursor()
            select: str = """SELECT * FROM users WHERE username = %s and password = %s and nome %s """
            cursor.execute(select, (username,generate_password_hash(password), nome))
            dati = cursor.fetchall()

            if dati:
               return redirect(url_for("personal")) 
            else:
                flash("nome, username o password errati")
                return redirect(url_for("login"))

            
        except Exception as e :
            flash(e)
            return redirect(url_for("login"))

       
        

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="register", header="register")
    elif request.method == "POST":
        
        credentials = get_request_params("nome","username", "cognome", "pswd", "pswdconf")
        

        if isEmpty(credentials.values()):
            flash("non ci possono essere campi vuoti")
            return redirect(url_for("register"))

        if credentials["pswd"] != credentials["pswdconf"]:
            flash("password non conformi")
            return redirect(url_for("register"))
        
        cursor = Mysql.connection.cursor()
        query: str= """SELECT * FROM users WHERE username  = %s """
        cursor.execute(query, (credentials["username"],))
        dati: tuple = cursor.fetchall()

       

        if dati:
            flash("utente gia esistente")
            return redirect(url_for("register"))
        
        

        query_insert = """
                INSERT INTO users (username, password, nome, cognome)
                VALUES
                (%s, %s, %s, %s)
                """
        credentials["pswd"] = generate_password_hash(credentials["pswd"])
       

        try:
            cursor.execute(query_insert, (credentials["username"], credentials["pswd"], credentials["nome"], credentials["cognome"]))
            Mysql.connection.commit()
            return redirect(url_for("personal"))
        except Exception as e:
            flash("c'é stato un problema con il db")
            return redirect(url_for("register"))

        
@app.route("/login"  ,methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo="login", header="login")
    elif request.method == "POST":
        credentials = get_request_params("username", "pswd")

        #print(username, pswd)
        
        if isEmpty(credentials.values()):
            flash("non ci possono essere campi vuoti")
            return redirect(url_for("login"))
        
        #hash_pswd = generate_password_hash(pswd)
        #dati = ()
        #print(hash_pswd)

        try:
            cursor = Mysql.connection.cursor()
            query = """SELECT * FROM users WHERE username = %s"""
            cursor.execute(query, (credentials["username"],))
            dati: tuple = cursor.fetchall()
            
            
                
            
            if not dati:
                flash("username o password non corretti")
                return redirect(url_for("login"))
            
            
            stored_hash_db = dati[0][1]
            
            

            if not check_password_hash(stored_hash_db, credentials["pswd"]):
                flash("username o password non corretti")
                return redirect(url_for("login"))


            
            return redirect(url_for("personal"))
        except:
            flash("c'é stato un problema con il db")
            return redirect(url_for("login"))







@app.route("/personal")
def personal():
    return render_template("personal.html")

app.run(debug=True)
