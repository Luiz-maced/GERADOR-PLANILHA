from . import db

class Treino(db.Model):
    ID_TREINO    = db.Column(db.Integer, primary_key=True)
    semana       = db.Column(db.String, nullable=False)
    agachamento  = db.Column(db.Float, nullable=False)
    supino       = db.Column(db.Float, nullable=False)
    lev_terra    = db.Column(db.Float, nullable=False)
    

