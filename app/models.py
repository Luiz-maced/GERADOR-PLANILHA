from . import db

class Treino(db.Model):
    ID_TREINO = db.Column(db.Integer, primary_key=True)
    agachamento = db.Column(db.Float, nullable=False)
    supino = db.Column(db.Float, nullable=False)
    lev_terra = db.Column(db.Float, nullable=False)
    

