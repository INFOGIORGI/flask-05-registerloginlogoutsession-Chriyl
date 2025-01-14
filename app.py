from flask import Flask, render_template, redirect, request, url_for # type: ignore
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_PASSWORD"] = "ospite"
app.config["MYSQL_DB"] = "w3schools"

Mysql= MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo="home", header="home")

@app.route("/logout")
def logout():
    return render_template("logout.html", titolo="logout", header="logout")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="register", header="register")
    elif request.method == "POST":
        nome: str = request.form.get("nome")
        username: str = request.form.get("username")
        cognome: str = request.form.get("cognome")
        pswd: str = request.form.get("pswd")
        pswdconf: str = request.form.get("pswdconf")
        print(nome, cognome, username, pswd, pswdconf)

        if pswd != pswdconf:
            return render_template("register.html", titolo="register", header="register", error="pswd non conformi")
        
        cursor: function = Mysql.connect.cursor()
        query: str= """SELECT * FROM users WHERE username  = %s """
        cursor.execute(query, (username,))
        dati: tuple = cursor.fetchall()

        print(dati)

        if dati:
            return render_template("register.html", titolo="register", header="register", error="utente gia esistente")

        query_insert = """
                INSERT INTO users (username, password, nome, cognome)
                VALUES
                (%s, %s, %s, %s)
                """
    
        cursor.execute(query_insert, (username, pswd, nome, cognome,))
        Mysql.connection.commit()
       
        return redirect(url_for("personal"))
    


        # eseguire query SELECT (email, pswd) FROM users WHERE users.email = email and users.pswd = pswd

        # condizione per verificare se esiste gia 

        # se esiste lancia errore al client

        # se non esiste ritorna la sessione, inserisce nel db e redirecta su /personal
            

        

@app.route("/login"  ,methods=["GET", "POST"])
def login():
    return render_template("login.html", titolo="login", header="login")


@app.route("/personal")
def personal():
    return render_template("personal.html")

app.run(debug=True)
