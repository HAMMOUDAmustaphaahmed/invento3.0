# createtables.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from models import db  # Assuming your models are defined in models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskadmin:Flask!1234@localhost:3306/invento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the db object to the app
db.init_app(app)

def create_tables_if_not_exists():
    with app.app_context():
        # Get the inspector for the current database
        inspector = inspect(db.engine)

        # List of table names that should exist
        expected_tables = ['user', 'articles', 'fournisseur', 'achats', 'ventes', 'demande_vente', 'demande_achat', 'history', 'usine']

        # Get the current existing tables in the database
        existing_tables = inspector.get_table_names()

        # Check for each expected table
        for table in expected_tables:
            if table not in existing_tables:
                print(f"Table '{table}' does not exist. Creating it...")
                db.create_all()  # This will create all tables defined in your models
                break  # Break after creating tables

        print("All tables checked/created.")

# Call the function to check and create tables
create_tables_if_not_exists()
