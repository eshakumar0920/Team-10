# models/loot_box.py
from datetime import datetime
from . import db

class LootBoxType(db.Model):
    """Defines different types of loot boxes that can be awarded"""
    __tablename__ = 'loot_box_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    tier = db.Column(db.Integer, default=1)  # Corresponds to the user's tier level
    icon_url = db.Column(db.String(255))
    
    # Relationship with loot boxes
    loot_boxes = db.relationship('LootBox', backref='type', lazy='dynamic')
    
    def __repr__(self):
        return f'<LootBoxType {self.name} (Tier {self.tier})>'


class LootBox(db.Model):
    """Tracks loot boxes in users' inventories"""
    __tablename__ = 'loot_boxes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('loot_box_types.id'), nullable=False)
    is_opened = db.Column(db.Boolean, default=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened_at = db.Column(db.DateTime, nullable=True)
    awarded_for = db.Column(db.String(100), nullable=True)  # e.g., "level_up", "event_participation"
    
    def __repr__(self):
        status = "Opened" if self.is_opened else "Unopened"
        return f'<LootBox {status} for user_id={self.user_id}>'
    
    def open(self):
        """Opens the loot box and awards its contents"""
        if not self.is_opened:
            self.is_opened = True
            self.opened_at = datetime.utcnow()
            
            # TODO: Logic to determine and award loot box contents
            # This could involve creating records in another table like user_items
            
            db.session.commit()
            return True
        return False