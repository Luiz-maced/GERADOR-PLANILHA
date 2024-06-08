from flask import Flask, send_file, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from openpyxl import Workbook
import os

app = Flask(__name__)

# Definindo o caminho do banco de dados para ser no diretório atual da aplicação
basedir                                      = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(basedir, 'uruk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db                                           = SQLAlchemy(app)

class Treino(db.Model):
    ID_TREINO   = db.Column(db.Integer, primary_key=True)
    semana      = db.Column(db.String,nullable=False)
    agachamento = db.Column(db.Float, nullable=False)
    supino      = db.Column(db.Float, nullable=False)
    lev_terra   = db.Column(db.Float, nullable=False)
  
# Crie todas as tabelas
with app.app_context():
    db.create_all()
    
@app.route('/adicionar_planilha', methods=['GET', 'POST'])
def adicionar_planilha():
    
    semana      = request.form.get('semana')
    agachamento = request.form.get('agachamento')
    supino      = request.form.get('supino')
    lev_terra   = request.form.get('lev_terra')

    if semana and agachamento and supino and lev_terra:
        novo_treino = Treino(semana=semana, agachamento=agachamento, supino=supino, lev_terra=lev_terra)
        db.session.add(novo_treino)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('preenche-planilha.html', error="Agachamento, Supino e Levantamento Terra são obrigatórios.")

@app.route('/menu', methods=['GET'])
def home():
    return render_template('menu.html')

@app.route('/gerar_planilha', methods=['GET'])
def gerar_planilha():
    # Verificar se o banco de dados está populado
    if not Treino.query.first():
        return "O banco de dados está vazio, por favor, alimente o formulario antes de clicar para gerar a planilha!."

    wb = Workbook()
    ws = wb.active
    ws.append(["semana", "Agachamento", "Supino", "Levantamento Terra"])
    
    treinos = Treino.query.all()
    for treino in treinos:
        ws.append([treino.semana, treino.agachamento, treino.supino, treino.lev_terra])
        
    wb_path = "planilha_de_treinos.xlsx"
    wb.save(wb_path)

    # Excluir os registros da tabela após o download da planilha
    Treino.query.delete()
    db.session.commit()

    return send_file(wb_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
