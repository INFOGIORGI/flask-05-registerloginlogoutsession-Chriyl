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
   ...

       
        

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="register", header="register")
    elif request.method == "POST":
        nome: str = request.form.get("nome", "")
        username: str = request.form.get("username", "")
        cognome: str = request.form.get("cognome", "")
        pswd: str = request.form.get("pswd", "")
        pswdconf: str = request.form.get("pswdconf", "")
        #print(nome, cognome, username, pswd, pswdconf)

        if isEmpty([nome,cognome,pswd, pswdconf,username]):
            flash("non ci possono essere campi vuoti")
            #return render_template("register.html", titolo="register", header="register", error="non ci possono essere campi vuoti")
            return redirect(url_for("register"))

        if pswd != pswdconf:
            flash("password non conformi")
            return redirect(url_for("register"))
        
        cursor = Mysql.connection.cursor()
        query: str= """SELECT * FROM users WHERE username  = %s """
        cursor.execute(query, (username,))
        dati: tuple = cursor.fetchall()

        #print(dati)

        if dati:
            flash("utente gia esistente")
            return redirect(url_for("register"))
        
        

        query_insert = """
                INSERT INTO users (username, password, nome, cognome)
                VALUES
                (%s, %s, %s, %s)
                """
        hashedPswd = generate_password_hash(pswd)
        #if check_password_hash(password=pswd, pwhash=hashedPswd):
        #    return render_template("register.html", titolo="register", header="register", error="c'é stato un problema con l'hash della pswd")

        try:
             
            cursor.execute(query_insert, (username, hashedPswd, nome, cognome))
            Mysql.connection.commit()
            return redirect(url_for("personal"))
        except Exception as e:
            flash(e)
            return redirect(url_for("register"))

        
@app.route("/login"  ,methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo="login", header="login")
    elif request.method == "POST":
        username = request.form.get("username", "")
        pswd = request.form.get("pswd", "")

        #print(username, pswd)
        
        if isEmpty([username,pswd]):
            flash("non ci possono essere campi vuoti")
            return redirect(url_for("login"))
        
        #hash_pswd = generate_password_hash(pswd)
        #dati = ()
        #print(hash_pswd)

        try:
            cursor = Mysql.connection.cursor()
            query = """SELECT * FROM users WHERE username = %s"""
            cursor.execute(query, (username,))
            dati: tuple = cursor.fetchall()
            
            
                
            
            if not dati:
                flash("username o password non corretti")
                return redirect(url_for("login"))
            
            
            stored_hash_db = dati[0][1]
            
            

            if not check_password_hash(stored_hash_db, pswd):
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
