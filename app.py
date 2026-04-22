from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# ------------------------
# CONEXÃO COM BANCO
# ------------------------
def get_db():
    conn = sqlite3.connect("simcomamor.db")
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------
# CRIAR / ATUALIZAR TABELA
# ------------------------
def criar_tabela():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS casais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            nome TEXT,
            data TEXT,
            local TEXT,
            foto TEXT
        )
    """)

    # adiciona colunas novas automaticamente
    try:
        conn.execute("ALTER TABLE casais ADD COLUMN data_criacao TEXT")
    except:
        pass

    try:
        conn.execute("ALTER TABLE casais ADD COLUMN data_validade TEXT")
    except:
        pass

    conn.commit()
    conn.close()


# 🚨 IMPORTANTE: roda no Render
criar_tabela()


# ------------------------
# ROTAS
# ------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/<casal>')
def site_casal(casal):

    conn = get_db()
    dados = conn.execute(
        "SELECT * FROM casais WHERE slug = ?",
        (casal,)
    ).fetchone()
    conn.close()

    if not dados:
        return "Casal não encontrado"

    return render_template("casal.html", dados=dados)


# ------------------------
# CRIAR CASAL
# ------------------------
@app.route('/criar', methods=['GET', 'POST'])
def criar_casal():

    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        local = request.form['local']
        plano = int(request.form.get('plano', 6))

        slug = nome.lower().replace(" ", "-")
        foto = "/static/img/capa_padrao.jpg"

        hoje = datetime.now()
        data_criacao = hoje.strftime("%d/%m/%Y")

        if plano == 6:
            validade = hoje + timedelta(days=180)
        else:
            validade = hoje + timedelta(days=365)

        data_validade = validade.strftime("%d/%m/%Y")

        conn = get_db()
        conn.execute("""
            INSERT INTO casais (slug, nome, data, local, foto, data_criacao, data_validade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (slug, nome, data, local, foto, data_criacao, data_validade))
        conn.commit()
        conn.close()

        return f"""
        <h2>Site criado com sucesso 💍</h2>
        <p><strong>{nome}</strong></p>
        <p>Válido até: <strong>{data_validade}</strong></p>
        <p><a href="/{slug}">Acessar site</a></p>
        <p>Renovação: admin@simcomamor.com.br</p>
        """

    return render_template("criar.html")


# ------------------------
# ADMIN
# ------------------------
@app.route('/admin')
def admin():

    conn = get_db()
    casais = conn.execute("SELECT * FROM casais").fetchall()
    conn.close()

    return render_template("admin.html", casais=casais)


# ------------------------
# START LOCAL
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)