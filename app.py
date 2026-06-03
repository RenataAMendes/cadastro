from flask import Flask, render_template

from models import init_db

app = Flask(__name__)

init_db()


@app.route("/")
def login():
    return render_template("login.html")


# @app.route("/home")
# def home():
#     return render_template("index.html")


# @app.route("/produtos")
# def produtos():
#     return render_template("produtos.html")


if __name__ == "__main__":
    app.run(debug=True)