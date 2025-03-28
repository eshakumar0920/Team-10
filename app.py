from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, initialize_default_data
from routes import events_bp, leveling_bp, rewards_bp
from config import config_by_name
import os

def create_app(config_name='dev'):
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(events_bp, url_prefix='/api')
    app.register_blueprint(leveling_bp, url_prefix='/api/leveling')
    app.register_blueprint(rewards_bp, url_prefix='/api/rewards')
    
    # Initialize default data after app context is available
    with app.app_context():
        # Uncomment the following line when using Flask-Migrate for the first time
        # db.create_all()
        
        # TEMPORARILY COMMENTED OUT FOR MIGRATION
        initialize_default_data()
        #pass
        
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    app.run(debug=True)