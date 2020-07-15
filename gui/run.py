### IMPORT REQUIRED PYTHON MODULES ###
import json
from flask import Flask, redirect, url_for
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from sqlalchemy.pool import StaticPool

### IMPORT CONFIG FILE ### 
with open("config.json") as config_file:
    config = json.load(config_file)

### CONNECT TO THE DATABASE ###
try:
    db_path = "sqlite:///" + config.get("database_file")
    db_engine = create_engine(
        db_path, 
        echo=False, 
        connect_args={'check_same_thread':False},
        poolclass=StaticPool)
    Session = sessionmaker(bind=db_engine)
    db_connection = Session()
except:
    print("There was an error connecting to the database...")

### IMPORT DATABASE MODELS ###
Base = declarative_base()
from project.models import model_employees

### CREATE DATABASE TABLES BASED ON MODELS ###
Base.metadata.create_all(db_engine) 

### DEFINE THE FLASK APP ###
app = Flask('project', static_url_path='')
app.debug = False

### ALLOW RELOAD OF TEMPLATE FILES DURING DEVELOPMENT ###
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

### SET DEFAULT ROUTE REDIRECT ###
@app.route('/')
def index_redirect():
    return redirect(url_for('employees_index'))

### IMPORT CONTROLLERS ###
from project.controllers import controller_employees

### START THE APP ###    
if __name__ == '__main__':    
    app.run(host="0.0.0.0",port="8080")