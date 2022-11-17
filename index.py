from flask import Flask, render_template, request, jsonify, make_response
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

        sql_query = '''
            CREATE TABLE IF NOT EXISTS tblRequisicoes (
                bID integer PRIMARY KEY,
                bTitulo text,
                bDataExpectativa text,
                bDescricao text,
                bObservacoes text
            );
        '''
        cursor.execute(sql_query)

        sql_query = '''
            CREATE TABLE IF NOT EXISTS tblAcompanhamento (
                cID integer PRIMARY KEY,
                cRequisicaoID text,
                cUsuarioID text,
                cStatus text,
                cData text
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

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Usuario cadastrado com sucesso</div>"
     })

    return make_response(response_data, 200)


@app.route('/dadosUsuario', methods = ['POST'])
def dadosUsuario():
    conn = db_connection()
    cursor = conn.cursor()
    usuarioID = request.get_json()['txtEditUsuarioID']

    sql_query = f"SELECT * FROM tblUsuarios WHERE aID = {usuarioID}"
    cursor = conn.execute(sql_query)
    usuario = cursor.fetchone()

    response_data = jsonify({
        'id': usuario[0],
        'nome': usuario[1],
        'email': usuario[2],
        'telefone': usuario[3],
        'profissao': usuario[4],
        'area': usuario[5]
    })

    resp = make_response(response_data, 200)
    return resp

@app.route('/editarUsuario', methods = ['POST'])
def editarUsuario():
    conn = db_connection()
    cursor = conn.cursor()

    id = request.form.get('txtEditusuarioID')
    nome = request.form.get('txtEditarNome')
    email = request.form.get('txtEditarEmail')
    contato = request.form.get('txtEditarContato')
    profissao = request.form.get('txtEditarProfissao')
    area = request.form.get('txtEditarArea')

    sql_query = f"UPDATE tblUsuarios SET aNome = '{nome}', aEmail = '{email}', aContato = '{contato}', aProfissao = '{profissao}', aArea = '{area}' WHERE aID = {id}"
    conn.execute(sql_query)
    conn.commit()

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Usuario modificado com sucesso</div>"
     })

    return make_response(response_data, 200)

@app.route('/deletarUsuario', methods = ['POST'])
def deletarUsuario():
    conn = db_connection()
    cursor = conn.cursor()
    usuarioID = request.form.get('txtDeleteusuarioID')

    sql_query = f"DELETE FROM tblUsuarios WHERE aID = {usuarioID}"
    cursor = conn.execute(sql_query)
    conn.commit()

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Usuario excluído com sucesso</div>"
     })

    return make_response(response_data, 200)

@app.route("/requisicoes/cadastrar", methods = ['POST', 'GET'])
def requisicoesCadastrar():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        titulo = request.form.get('txtCadastrarTitulo')
        dataExpectativa = request.form.get('txtCadastrarDataExpectativa')
        descricao = request.form.get('txtCadastrarDescricao')
        observacoes = request.form.get('txtCadastrarObservacoes')
        
        sql_query = f"""
        INSERT INTO tblRequisicoes(bTitulo, bDataExpectativa, bDescricao, bObservacoes) 
        VALUES ('{titulo}', '{dataExpectativa}', '{descricao}', '{observacoes}');
        INSERT INTO tblAcompanhamento(cRequisicaoID, cUsuarioID, cStatus, cData)
        VALUES (last_insert_rowid(), NULL, 'NOVO', DATETIME());
        """
        conn.executescript(sql_query)
        conn.commit()
        response_data = jsonify({
            'title': "Confirmação",
            'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Requisição cadastrada com sucesso</div>"
        })

        return make_response(response_data, 200)
    return render_template('requisicoes.cadastrar.html')

@app.route("/requisicoes/novas")
def novasRequisicoes():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("""
        SELECT  
            tblRequisicoes.bID,
            tblRequisicoes.bTitulo,
            tblAcompanhamento.cStatus,
            strftime('%d/%m/%Y %H:%M:%S', tblAcompanhamento.cData)
        FROM tblRequisicoes
        LEFT JOIN tblAcompanhamento
        ON      tblAcompanhamento.cID =
                (
                SELECT  cID
                FROM    tblAcompanhamento
                WHERE   tblRequisicoes.bID = tblAcompanhamento.cRequisicaoID
                ORDER BY
                        tblAcompanhamento.cID DESC
                LIMIT   1
                )
        WHERE tblAcompanhamento.cStatus = 'NOVO'
    """)
    requisicoes = [
        dict(id=row[0], titulo=row[1], status=row[2], data=row[3])
        for row in cursor.fetchall()
    ]
    return render_template('requisicoes.novas.html', requisicoes=requisicoes)

@app.route("/requisicoes/detalhes/<id>/<origem>")
def requisicoesDetalhes(id, origem):
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute(f"""
        SELECT  *
        FROM tblRequisicoes
        LEFT JOIN tblAcompanhamento
        ON      tblAcompanhamento.cID =
                (
                SELECT  cID
                FROM    tblAcompanhamento
                WHERE   tblRequisicoes.bID = tblAcompanhamento.cRequisicaoID
                ORDER BY
                        tblAcompanhamento.cID DESC
                LIMIT   1
                )
        WHERE tblRequisicoes.bID = {id}
    """)
    requisicao = cursor.fetchone()

    cursor = conn.execute("SELECT * FROM tblUsuarios")
    usuarios = [
        dict(id=row[0], nome=row[1], email=row[2], contato=row[3], profissao=row[4], area=row[5])
        for row in cursor.fetchall()
    ]

    cursor = conn.execute(f"SELECT cID, cRequisicaoID, cUsuarioID, cStatus, strftime('%d/%m/%Y %H:%M:%S', cData), aNome FROM tblAcompanhamento LEFT JOIN tblUsuarios ON tblUsuarios.aID = tblAcompanhamento.cUsuarioID WHERE cRequisicaoID = {id}")
    historicos = [
        dict(id=row[0], requisicaoID=row[1], usuarioID=row[2], status=row[3], data=row[4], nome=row[5])
        for row in cursor.fetchall()
    ]

    return render_template('requisicoes.detalhes.html', requisicao=requisicao, usuarios=usuarios, historicos=historicos, origem=origem)

@app.route('/requisicoes/analisar', methods = ['POST'])
def analisarRequisicao():
    conn = db_connection()
    cursor = conn.cursor()
    requisicaoID = request.form.get('txtAnalisarRequisicaoID')
    usuarioID = request.form.get('txtAnalisarUsuarioID')

    sql_query = f"INSERT INTO tblAcompanhamento(cRequisicaoID, cUsuarioID, cStatus, cData) VALUES ({requisicaoID}, {usuarioID}, 'EM ANALISE', DATETIME())"
    cursor = conn.execute(sql_query)
    conn.commit()

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Status atualizado com sucesso</div>"
     })

    return make_response(response_data, 200)

@app.route("/requisicoes/emAnalise")
def requisicoesEmAndamento():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("""
        SELECT  
            tblRequisicoes.bID,
            tblRequisicoes.bTitulo,
            tblAcompanhamento.cStatus,
            strftime('%d/%m/%Y %H:%M:%S', tblAcompanhamento.cData),
            tblUsuarios.aNome
        FROM tblRequisicoes
        LEFT JOIN tblAcompanhamento
        ON  tblAcompanhamento.cID =
            (
            SELECT  cID
            FROM    tblAcompanhamento
            WHERE   tblRequisicoes.bID = tblAcompanhamento.cRequisicaoID
            ORDER BY
                    tblAcompanhamento.cID DESC
            LIMIT   1
            )
        LEFT JOIN tblUsuarios
        ON  tblUsuarios.aID = tblAcompanhamento.cUsuarioID  
        WHERE tblAcompanhamento.cStatus = 'EM ANALISE'
    """)

    requisicoes = [
        dict(id=row[0], titulo=row[1], status=row[2], data=row[3], nome=row[4])
        for row in cursor.fetchall()
    ]
    return render_template('requisicoes.em.analise.html', requisicoes=requisicoes)

@app.route('/requisicoes/concluir', methods = ['POST'])
def concluirRequisicao():
    conn = db_connection()
    cursor = conn.cursor()
    requisicaoID = request.form.get('txtConcluirRequisicaoID')
    usuarioID = request.form.get('txtConcluirUsuarioID')

    sql_query = f"INSERT INTO tblAcompanhamento(cRequisicaoID, cUsuarioID, cStatus, cData) VALUES ({requisicaoID}, {usuarioID}, 'CONCLUIDO', DATETIME())"
    cursor = conn.execute(sql_query)
    conn.commit()

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Status atualizado com sucesso</div>"
     })

    return make_response(response_data, 200)

@app.route("/requisicoes/concluidas")
def requisicoesConcluidas():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("""
        SELECT  
            tblRequisicoes.bID,
            tblRequisicoes.bTitulo,
            tblAcompanhamento.cStatus,
            strftime('%d/%m/%Y %H:%M:%S', tblAcompanhamento.cData),
            tblUsuarios.aNome
        FROM tblRequisicoes
        LEFT JOIN tblAcompanhamento
        ON  tblAcompanhamento.cID =
            (
            SELECT  cID
            FROM    tblAcompanhamento
            WHERE   tblRequisicoes.bID = tblAcompanhamento.cRequisicaoID
            ORDER BY
                    tblAcompanhamento.cID DESC
            LIMIT   1
            )
        LEFT JOIN tblUsuarios
        ON  tblUsuarios.aID = tblAcompanhamento.cUsuarioID  
        WHERE tblAcompanhamento.cStatus = 'CONCLUIDO'
    """)

    requisicoes = [
        dict(id=row[0], titulo=row[1], status=row[2], data=row[3], nome=row[4])
        for row in cursor.fetchall()
    ]
    return render_template('requisicoes.concluidas.html', requisicoes=requisicoes)

@app.route('/requisicoes/editar', methods = ['POST'])
def editarRequisicao():
    conn = db_connection()
    cursor = conn.cursor()
    requisicaoID = request.form.get('txtEditarRequisicaoID')
    titulo = request.form.get('txtEditarTituloRequisicao')
    dataExpectativa = request.form.get('txtEditarDataExpectativa')
    descricao = request.form.get('txtEditarDescricao')
    observacoes = request.form.get('txtEditarObservacoes')

    sql_query = f"UPDATE tblRequisicoes SET bTitulo = '{titulo}', bDataExpectativa = '{dataExpectativa}', bDescricao = '{descricao}', bObservacoes = '{observacoes}' WHERE bID = {requisicaoID}"
    cursor = conn.execute(sql_query)
    conn.commit()

    response_data = jsonify({
        'title': "Confirmação",
        'body': "<div class='text-center text-success'><i class='fas fa-check fa-4x mb-3'></i></div><div class='text-black'>Requisição atualizada com sucesso</div>"
     })

    return make_response(response_data, 200)



if __name__ == "__main__":
    app.run(debug=True)