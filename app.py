from flask import Flask, render_template
import sqlite3
from flask import request, redirect

app = Flask(__name__)

# ------------------------
# CONEXÃO COM BANCO
# ------------------------
def get_db():
    conn = sqlite3.connect("simcomamor.db")
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------
# CRIAR TABELA
# ------------------------
def criar_tabela():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS casais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            nome TEXT,
            data TEXT,
            local TEXT
        )
    """)
    conn.commit()
    conn.close()


# ------------------------
# INSERIR CASAL INICIAL
# ------------------------
def inserir_casal():
    conn = get_db()
    conn.execute("""
        INSERT OR IGNORE INTO casais (slug, nome, data, local)
        VALUES (?, ?, ?, ?)
    """, ("ana-e-joao", "Ana & João", "12 de Outubro de 2026", "Rio de Janeiro - RJ"))
    conn.commit()
    conn.close()


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

# =================
# RSVP
# =================
@app.route('/rsvp')
def rsvp():
    return "RSVP em construção"

# =================
# PRESENTES
# =================
@app.route('/presentes')
def presentes():
    return "Lista de presentes em construção"

# =================
# ÁLBUM
# =================
@app.route('/album')
def album():
    return "Álbum em construção"

# =================
# RECADOS
# =================
@app.route('/recados')
def recados():
    return "Mural de recados em construção"

# =================
# AGENDA
# =================
@app.route('/agenda')
def agenda():
    return "Agenda em construção"

# =================
# LOCALIZAÇÃO
# =================
@app.route('/localizacao')
def localizacao():
    return "Localização em construção"

# =================
# HISTÓRIA
# =================
@app.route('/historia')
def historia():
    return "História do casal em construção"

# =================
# CONVITE
# =================
@app.route('/convite')
def convite():
    return "Convite digital em construção"

# =================
# CERIMÔNIA
# =================
@app.route('/cerimonia')
def cerimonia():
    return "Cerimônia em construção"

# =================
# MÚSICAS
# =================
@app.route('/musicas')
def musicas():
    return "Músicas em construção"

# =================
# MAIS OPÇÕES
# =================
@app.route('/mais')
def mais():
    return "Mais opções em construção"

# =================
# CRIAR SITE DO CASAL
# =================
@app.route('/criar', methods=['GET', 'POST'])
def criar_casal():

    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        local = request.form['local']

        # cria slug automático
        slug = nome.lower().replace(" ", "-")

        conn = get_db()
        conn.execute("""
            INSERT INTO casais (slug, nome, data, local)
            VALUES (?, ?, ?, ?)
        """, (slug, nome, data, local))
        conn.commit()
        conn.close()

        return redirect(f'/{slug}')

    return render_template("criar.html")

# ------------------------
# START
# ------------------------
if __name__ == '__main__':
    criar_tabela()
    inserir_casal()
    app.run(debug=True)