from flask import render_template, redirect, url_for, request, session, flash
from app import app
from models import Usuario, cadastrar_usuario


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if  request.method == 'POST':

        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        funcao = request.form.get('funcao')

        if Usuario.query.filter_by(email=email).first():
            flash(
                'Este e-mail já está cadastrado!',
                'danger'
            )

            return redirect(url_for('cadastro'))
        
        try:
            cadastrar_usuario(nome=nome, email=email, senha=senha)
            
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash('Erro ao cadastrar usuário. Tente novamente.', 'danger')
            return redirect(url_for('cadastro'))

    
    return render_template('cadastro.html')
        
        