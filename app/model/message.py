from app import db
from datetime import datetime
from app.model.user import User


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_msg = db.Column(db.String(255), nullable=False)
    bot_response = db.Column(db.String(255), nullable=False)
    user_timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    bot_timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id, ondelete='CASCADE'))

    def __repr__(self):
        return '<Message {}>'.format(self.name)