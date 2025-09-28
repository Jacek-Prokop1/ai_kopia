from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime

db = SQLAlchemy()

class KnowledgeItem(db.Model):
    __tablename__ = 'knowledge_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='inne')
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(JSON, nullable=True)
    embedding = db.Column(db.PickleType, nullable=True)
    lang = db.Column(db.String(5), nullable=False, default="pl")
    embedding = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<KnowledgeItem(id={self.id}, title={self.title}, category={self.category})>"
    
class ChatFeedback(db.Model):
    __tablename__ = "chat_feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(36), nullable=False)
    user_question = db.Column(db.Text, nullable=True) 
    ai_response = db.Column(db.Text, nullable=False)  
    rating = db.Column(db.Enum("up", "down"), nullable=True)
    lang = db.Column(db.String(5), nullable=False, default="pl")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_confirmed = db.Column(db.Boolean, nullable=True, default=None)  

    def __repr__(self):
        return f"<ChatFeedback(id={self.id}, session={self.session_id}, rating={self.rating}, admin_confirmed={self.admin_confirmed})>"

