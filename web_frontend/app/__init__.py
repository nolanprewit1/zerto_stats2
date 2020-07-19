### IMPORT REQUIRED PYTHON MODULES ###
import json, os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from sqlalchemy.pool import StaticPool

### IMPORT CONFIG FILE ### 
load_dotenv(os.path.join( os.getcwd(), '..', '.env' ))

### CONNECT TO THE DATABASE ###
try:
    db_path = "sqlite:///" + os.getenv("database_file")
    db_engine = create_engine(
        db_path, 
        echo=False, 
        connect_args={"check_same_thread":False},
        poolclass=StaticPool)
    Session = sessionmaker(bind=db_engine)
    db_connection = Session()
except:
    print("There was an error connecting to the database...")

### IMPORT DATABASE MODELS ###
from app.models.models_monitoring_alerts import MonitoringAlerts
from app.models.models_monitoring_events import MonitoringEvents

### CREATE DATABASE TABLES BASED ON MODELS ###
declarative_base().metadata.create_all(db_engine) 

### DEFINE THE FLASK APP ###
app = Flask(__name__, static_url_path='',template_folder='views')
app.debug = False

### ALLOW RELOAD OF TEMPLATE FILES DURING DEVELOPMENT ###
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

### IMPORT CONTROLLERS ###
from app.controllers import index
from app.controllers import monitoring_alerts