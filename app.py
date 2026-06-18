from flask import Flask, render_template, request, redirect, url_for
from models import init_db, realizar_login
from routes.cadastro_produto import registrar_rotas

app = Flask(__name__)

init_db()

registrar_rotas(app)

@app.route("/")
def tela_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = realizar_login(email, senha)

    if usuario:
        return redirect(url_for("home"))

    return "Usuário ou senha inválidos"

@app.route("/home")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)