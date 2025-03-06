# models/level.py
from . import db

class Level(db.Model):
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)
    xp_required = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    perks = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Level {self.level_number}: {self.title}>'
