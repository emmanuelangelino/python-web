import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from contextlib import closing

DATABASE = "/tmp/blog.db"
SECRET_KEY = "ocean fullstack"
USERNAME = "admin"
PASSWORD = "fevereiro"

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config["DATABASE"])

def criar_bd():
    with closing(conectar_bd()) as bd:
        with app.open_resource('esquema.sql') as sql:
            bd.cursor().executescript(sql.read())
        bd.commit()

# POSTS MOCK
posts = [
    {
        "titulo": "Post 1",
        "texto": "Meu primeito post"
    },
    {
        "titulo": "Post 2",
        "texto": "Meu segundo post"
    },
    {
        "titulo": "Post 3",
        "texto": "Meu terceiro post"
    }
]

@app.route("/")
def exibir_entradas():
    return render_template("exibir_entradas.html", entradas=posts)

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    novo_post = {
        "titulo": request.form['titulo'],
        "texto": request.form['texto']
    }
    posts.append(novo_post)  
    return redirect(url_for('exibir_entradas'))

@app.route("/login", methods=["GET","POST"])
def login():
    erro = ""
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logado"] = True
            flash("Login efetuado com sucesso!")
            return redirect(url_for("exibir_entradas"))
        erro = "Usuário ou senha inválidos."
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.pop("logado",None)
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("exibir_entradas"))