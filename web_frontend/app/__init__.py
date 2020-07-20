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
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(os.getenv("database_username"), os.getenv("database_password"), os.getenv("database_hostname"), os.getenv("database_port"), os.getenv("database_name"))
    db_engine = create_engine(url, client_encoding='utf8')
    Session = sessionmaker(bind=db_engine)
    db_connection = Session()
except:
    print("There was an error connecting to the database...")

### IMPORT DATABASE MODELS ###
from app.models.models_monitoring_alerts import MonitoringAlerts
from app.models.models_monitoring_events import MonitoringEvents

### DEFINE THE FLASK APP ###
app = Flask(__name__, static_url_path='',template_folder='views', static_folder="static")
app.debug = False

### ALLOW RELOAD OF TEMPLATE FILES DURING DEVELOPMENT ###
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

### IMPORT CONTROLLERS ###
from app.controllers import index
from app.controllers import monitoring_alerts
from app.controllers import monitoring_events