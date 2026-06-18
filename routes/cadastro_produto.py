from flask import render_template, request, redirect, url_for
from models import cadastrar_produto

def registrar_rotas(app):

    @app.route("/produtos")
    def produtos():
        return render_template("produtos.html")

    # @app.route("/cadastro_produtos")
    # def cadastro_produtos():
    #     return render_template("cadastro_produtos.html")


    # @app.route("/salvar_produto", methods=["POST"])
    # def salvar_produto():

    #     cadastrar_produto(
    #         nome_produto=request.form.get("nome"),
    #         quantidade=int(request.form.get("quantidade")),
    #         descricao=request.form.get("descricao"),
    #         marca_produto=request.form.get("marca"),
    #         id_categoria="",
    #         id_user=""
    #     )
        

    #     return redirect(url_for("cadastro_produtos"))