from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('db_SIRS.sqlite')
        cursor = conn.cursor()
        sql_query = '''
            CREATE TABLE IF NOT EXISTS tblUsuarios (
                aID integer PRIMARY KEY,
                aNome text,
                aEmail text,
                aContato text,
                aProfissao text,
                aArea text
            );
        '''
        cursor.execute(sql_query)
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/usuarios")
def usuarios():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM tblUsuarios")
    usuarios = [
        dict(id=row[0], nome=row[1], email=row[2], contato=row[3], profissao=row[4], area=row[5])
        for row in cursor.fetchall()
    ]
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/cadastroUsuario', methods = ['POST']) 
def cadastroUsuario():
    conn = db_connection()
    cursor = conn.cursor()
    nome = request.form.get('txtCadastrarNome')
    email = request.form.get('txtCadastrarEmail')
    contato = request.form.get('txtCadastrarContato')
    profissao = request.form.get('txtCadastrarProfissao')
    area = request.form.get('txtCadastrarArea')
    
    sql_query = "INSERT INTO tblUsuarios(aNome, aEmail, aContato, aProfissao, aArea) VALUES (?, ?, ?, ?, ?)"
    conn.execute(sql_query, (nome, email, contato, profissao, area))
    conn.commit()

    return request.form

if __name__ == "__main__":
    app.run(debug=True)