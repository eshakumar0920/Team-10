from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate  # Add this import
from models import db, initialize_default_data
from routes import events_bp, leveling_bp, rewards_bp
from routes.auth import auth_bp #Import the new authentication blueprint
from config import config_by_name
import os

def create_app(config_name='dev'):
    app = Flask(__name__)
    #CORS(app)
    CORS(app, origins=["http://localhost:8080"])

    
    # Load config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(events_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth routes
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
    #app.run(debug=True)

    # Prints all registered routes for debugging
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - Methods: {rule.methods}")

    app.run(debug=True)