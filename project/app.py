import os
from flask import Flask
from models import db
from chat import chat_bp
from admin import admin_bp
from dotenv import load_dotenv
from openai import OpenAI
from feedback import feedback_bp
from admin_feedback import admin_feedback_bp

#  $env:OPENAI_API_KEY = "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"
# python .\project\app.py
load_dotenv()  

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Nie znaleziono OPENAI_API_KEY w środowisku!")

client = OpenAI(api_key=api_key)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp, url_prefix="/feedback")
app.register_blueprint(admin_feedback_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
