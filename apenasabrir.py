from flask import Flask,url_for,render_template
app= Flask(__name__)

@app.route("/")
def iniciar():
    return render_template("editar_usuarios.html")

if __name__ == "__main__":
    app.run(debug=True)