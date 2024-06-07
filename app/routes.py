from flask import render_template, request, redirect, url_for, send_file
from . import db
from .models import Treino
from openpyxl import Workbook
import os

from flask import current_app as app  # Usar a instância do aplicativo

@app.route('/adicionar_planilha', methods=['GET', 'POST'])
def adicionar_planilha():
    agachamento = request.form.get('agachamento')
    supino = request.form.get('supino')
    lev_terra = request.form.get('lev_terra')

    if agachamento and supino and lev_terra:
        novo_treino = Treino(agachamento=agachamento, supino=supino, lev_terra=lev_terra)
        db.session.add(novo_treino)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('preenche-planilha.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('menu.html')

@app.route('/gerar_planilha', methods=['GET'])
def gerar_planilha():
    # Verificar se o banco de dados está populado
    if not Treino.query.first():
        return "O banco de dados está vazio. Não há dados para baixar."
        
    wb = Workbook()
    ws = wb.active
    ws.append(["Supino", "Agachamento", "Levantamento Terra", "Exercicios"])

    treinos = Treino.query.all()
    for treino in treinos:
        exercicios = ', '.join([exercicio.nome for exercicio in treino.exercicios])
        ws.append([treino.supino, treino.agachamento, treino.lev_terra, exercicios])
        
    # Diretório para salvar a planilha (dentro do diretório do projeto)
    gerar_planilhas = os.path.join(app.root_path, 'gerar_planilhas')
    if not os.path.exists(gerar_planilhas):
     os.makedirs(gerar_planilhas)

    wb_path = os.path.join(gerar_planilhas, "planilha_de_treinos.xlsx")
    wb.save(wb_path)

    # Excluir os registros da tabela após o download da planilha
    Treino.query.delete()
    db.session.commit()

    return send_file(wb_path, as_attachment=True)