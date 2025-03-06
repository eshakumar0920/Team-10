from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate  # Add this import
from models import db
from routes import events_bp
from config import config_by_name
import os

def create_app(config_name='dev'):
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # Add this line
    
    # Register blueprints
    app.register_blueprint(events_bp, url_prefix='/api')
    
    # Comment out or remove this block when using Flask-Migrate
    # With Flask-Migrate, you'll use commands instead of auto-creating tables
    # with app.app_context():
    #     db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run(debug=True)
