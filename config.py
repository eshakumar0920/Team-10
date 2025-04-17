#### config/config.py
import os
from supabase import create_client #Import create_client from supabase

class Config:
    """Base config class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://eventadmin:your_password@localhost/events_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Supabase Configuration Variables
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://lzcpjxkttpfcgcwonrfc.supabase.co')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx6Y3BqeGt0dHBmY2djd29ucmZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMwMDQ3MjgsImV4cCI6MjA1ODU4MDcyOH0.ShKvEPSEEaT6jbvJ4yl56vemZhSYhY0jL5rgRI4duHc')

    #Initialize Supabase Client
    SUPABASE_CLIENT = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Function to get the Supabase client instance
    @classmethod
    def get_supabase_client(cls):
        return cls.SUPABASE_CLIENT

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
