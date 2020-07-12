### IMPORT REQUIRED PYTHON MODULES ###
import json
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from sqlalchemy.pool import StaticPool

### IMPORT CONFIG FILE ### 
with open("..\config.json") as config_file:
    config = json.load(config_file)

### CONNECT TO THE DATABASE ###
try:
    db_path = "sqlite:///" + config.get("database_file")
    db_engine = create_engine(
        db_path, 
        echo=True, 
        connect_args={'check_same_thread':False},
        poolclass=StaticPool)
    Session = sessionmaker(bind=db_engine)
    db_connection = Session()
except:
    print("There was an error connecting to the database...")

### CREATE CLASSES THAT MATCH DATABASE TABLES ###
Base = declarative_base()
class MonitoringAlerts(Base):
    __tablename__ = 'monitoring_alerts'
    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    collectionTime = Column(String)

### CREATE DATABASE TABLES BASED ON MODELS ###
Base.metadata.create_all(db_engine) 