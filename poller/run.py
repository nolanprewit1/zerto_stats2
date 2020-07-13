### IMPORT REQUIRED PYTHON MODULES ###
import json
import requests
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
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
        echo=False, 
        connect_args={"check_same_thread":False},
        poolclass=StaticPool)
    Session = sessionmaker(bind=db_engine)
    db_connection = Session()
except:
    print("There was an error connecting to the database...")

### CREATE CLASSES THAT MATCH DATABASE TABLES ###
Base = declarative_base()
class MonitoringAlerts(Base):
    __tablename__ = "monitoring_alerts"
    Id = Column(Integer, primary_key=True)
    Identifier = Column(String, unique=True, nullable=False)
    Type = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    CollectionTime = Column(String, unique=False, nullable=False)

### CREATE DATABASE TABLES BASED ON MODELS ###
Base.metadata.create_all(db_engine) 

### FUNCTION TO AUTHENTICATE WITH ZERTO ANALYTICS API AND RETURN AUTHORIZATION TOKEN ###
def getAuthorizationToken ():
    url = config.get("zerto_analytics_url") + "auth/token"
    data = {
        "username": config.get("zerto_analytics_username"),
        "password": config.get("zerto_analytics_password")
    }
    response = requests.post(url, json=data)
    return json.loads(response.content)["token"]

### GET MONITORING ALERTS ###
def getMonitoringAlerts (api_token):
    url = config.get("zerto_analytics_url") + "monitoring/alerts"
    headers = {"Authorization": "Bearer " + api_token }
    response = requests.get(url, headers=headers)
    content = json.loads(response.content)
    for item in content:
        data = MonitoringAlerts(
            Identifier = item["identifier"],
            Type = item["type"],
            Description = item["description"],
            SiteName = item["site"]["name"],
            CollectionTime = item["collectionTime"]
        )
        db_connection.add(data)
        
    db_connection.commit()

api_token = getAuthorizationToken()
getMonitoringAlerts(api_token)