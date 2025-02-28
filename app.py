from flask import Flask
from flask_cors import CORS
from models import db
from routes import events_bp
from config.config import config_by_name
import os

def create_app(config_name='dev'):
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(events_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run(debug=True)
