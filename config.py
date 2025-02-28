#### config/config.py
```python
import os

class Config:
    """Base config class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://eventadmin:your_password@localhost/events_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True

class TestingConfig(Config):
    """Testing config"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://eventadmin:your_password@localhost/test_events_db'

class ProductionConfig(Config):
    """Production config"""
    # Production specific settings

# Export the config based on environment
config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}
