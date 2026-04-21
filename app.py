from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<casal>')
def site_casal(casal):
    return render_template("casal.html", casal=casal)

@app.route('/rsvp')
def rsvp():
    return "RSVP em construção"

@app.route('/presentes')
def presentes():
    return "Lista de presentes em construção"

@app.route('/album')
def album():
    return "Álbum em construção"

@app.route('/recados')
def recados():
    return "Mural de recados em construção"

@app.route('/agenda')
def agenda():
    return "Agenda em construção"

@app.route('/localizacao')
def localizacao():
    return "Localização em construção"

@app.route('/historia')
def historia():
    return "História do casal em construção"

@app.route('/convite')
def convite():
    return "Convite digital em construção"

@app.route('/cerimonia')
def cerimonia():
    return "Cerimônia em construção"

@app.route('/musicas')
def musicas():
    return "Músicas em construção"

@app.route('/mais')
def mais():
    return "Mais opções em construção"

if __name__ == '__main__':
    app.run()