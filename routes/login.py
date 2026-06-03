from flask import render_template, redirect, url_for, request, session, flash
from models import Usuario


def login_routes(app):

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if "usuario_id" in session:
            return redirect(url_for("index"))

        if request.method == "POST":
            email = request.form.get("email")
            senha = request.form.get("senha")

            usuario = Usuario.query.filter_by(email=email, senha=senha).first()

            if usuario:
                session["usuario_id"] = usuario.id
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("index"))
            else:
                flash("E-mail ou senha incorretos.", "danger")

        return render_template("login.html")


    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))