# check_db_user.py
from flask import Flask
from models import db
from sqlalchemy import text
import os
from config import config_by_name  # Import your app's config

# Create a minimal Flask app for testing
app = Flask(__name__)

# Use the same configuration as your main app
config_name = os.getenv('FLASK_ENV', 'dev')
app.config.from_object(config_by_name[config_name])

# Initialize the database
db.init_app(app)

def check_db_user():
    with app.app_context():
        try:
            # Query current user and session user
            result = db.session.execute(text("SELECT current_user, session_user;")).fetchone()
            print(f"Current PostgreSQL user: {result[0]}")
            print(f"Session PostgreSQL user: {result[1]}")
            
            # Try to get user permissions
            permissions = db.session.execute(text("""
                SELECT rolname, rolsuper, rolcreaterole, rolcreatedb 
                FROM pg_roles 
                WHERE rolname = current_user;
            """)).fetchone()
            
            if permissions:
                print(f"Username: {permissions[0]}")
                print(f"Superuser: {permissions[1]}")
                print(f"Can create roles: {permissions[2]}")
                print(f"Can create databases: {permissions[3]}")
            
            # Check ownership of tables
            tables = db.session.execute(text("""
                SELECT tablename, tableowner 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                LIMIT 10;
            """)).fetchall()
            
            print("\nTable ownership (first 10 tables):")
            for table in tables:
                print(f"Table: {table[0]}, Owner: {table[1]}")
                
            # Test table creation permission
            try:
                db.session.execute(text("CREATE TABLE _test_permissions (id serial PRIMARY KEY);"))
                print("\nYou have CREATE TABLE permissions!")
                # Clean up
                db.session.execute(text("DROP TABLE _test_permissions;"))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"\nYou don't have CREATE TABLE permissions: {str(e)}")
                
        except Exception as e:
            print(f"Error checking database user: {str(e)}")

if __name__ == "__main__":
    check_db_user()