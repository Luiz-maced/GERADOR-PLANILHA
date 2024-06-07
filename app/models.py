from . import db

class Treino(db.Model):
    ID_TREINO = db.Column(db.Integer, primary_key=True)
    agachamento = db.Column(db.Float, nullable=False)
    supino = db.Column(db.Float, nullable=False)
    lev_terra = db.Column(db.Float, nullable=False)
    exercicios = db.relationship('Exercicio', backref='treino', lazy=True)

class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    treino_id = db.Column(db.Integer, db.ForeignKey('treino.ID_TREINO'))
