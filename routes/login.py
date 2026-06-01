from flask import render_template, redirect, url_for, request, session, flash
from models import Usuario


def login_routes(app):

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form.get("email")
            senha = request.form.get("senha")

            # procura usuário comum
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and usuario.senha == senha:
                session.clear()
                session["usuario_id"] = usuario.id
                session["tipo"] = "usuario"
                return redirect(url_for("home"))

            flash("Login inválido")

        return render_template("login.html")


    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))