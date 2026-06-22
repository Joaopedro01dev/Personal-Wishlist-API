from factory import db
from sqlalchemy import text

class WishlistItem(db.Model):
    __tablename__ = "WishlistItem"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(128), nullable=True)
    purchased = db.Column(db.Boolean, nullable=False, default=False, server_default=text("0"))
    sort_order = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Item {self.name}>"