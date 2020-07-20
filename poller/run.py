### IMPORT REQUIRED PYTHON MODULES ###
import json, requests, time, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm.exc import NoResultFound
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

Base = declarative_base()

### IMPORT DATABASE MODELS ###
class MonitoringAlerts(Base):
    __tablename__ = "monitoring_alerts"
    Id = Column(Integer, primary_key=True)
    Identifier = Column(String, unique=False, nullable=False)
    Type = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    CollectionTime = Column(DateTime, unique=False, nullable=False)
    PollTime = Column(DateTime, unique=False, nullable=False)

class MonitoringEvents(Base):
    __tablename__ = "monitoring_events"
    Id = Column(Integer, primary_key=True)
    Identifier = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    Code = Column(String, unique=False, nullable=False)
    OccurredOn = Column(DateTime, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    ZorgName = Column(String, unique=False, nullable=True)    
    PollTime = Column(DateTime, unique=False, nullable=False)

### CREATE DATABASE TABLES BASED ON MODELS ###
Base.metadata.create_all(db_engine) 

### FUNCTION TO AUTHENTICATE WITH ZERTO ANALYTICS API AND RETURN AUTHORIZATION TOKEN ###
def getAuthorizationToken ():
    url = os.getenv("zerto_analytics_url") + "auth/token"
    data = {
        "username": os.getenv("zerto_analytics_username"),
        "password": os.getenv("zerto_analytics_password")
    }
    response = requests.post(url, json=data)
    if(response.status_code != 200):
        print("Issue authorizing against Zerto Analytics API...")
        exit()
        
    return json.loads(response.content)["token"]

### GET MONITORING ALERTS ###
def getMonitoringAlerts (api_token, poll_time):
    url = os.getenv("zerto_analytics_url") + "monitoring/alerts"
    url_headers = {"Authorization": "Bearer " + api_token }
    response = requests.get(url, headers=url_headers)
    response_content = json.loads(response.content)
    for item in response_content:
        # Check for existing identifier
        try:
            results = db_connection\
                .query(MonitoringAlerts)\
                .filter(MonitoringAlerts.Identifier==item["identifier"])\
                .one()
        # If its a new alert save to database
        except NoResultFound:
            # Get the collectionTime, a string, and remove the last 5 characters then convert it ot a python datetime object 
            collection_time = datetime.strptime(item["collectionTime"][:-5], '%Y-%m-%dT%H:%M:%S')
            data = MonitoringAlerts(
                Identifier = item["identifier"],
                Type = item["type"],
                Description = item["description"],
                SiteName = item["site"]["name"],
                CollectionTime = collection_time,
                PollTime = poll_time
            )
            db_connection.add(data)
        
    # Save all collected data to the database
    db_connection.commit()

### GET MONITORING EVENTS ###
def getMonitoringEvents (api_token, poll_time):
    url = os.getenv("zerto_analytics_url") + "monitoring/events"
    url_headers = {"Authorization": "Bearer " + api_token }
    response = requests.get(url, headers=url_headers)
    response_content = json.loads(response.content)
    for item in response_content["events"]:
        # Check for existing identifier
        try:
            results = db_connection\
                .query(MonitoringEvents)\
                .filter(MonitoringEvents.Identifier==item["identifier"])\
                .one()
        # If its a new alert save to database
        except NoResultFound:
            # Get the collectionTime, a string, and remove the last 5 characters then convert it ot a python datetime object 
            occured_on = datetime.strptime(item["occurredOn"][:-5], '%Y-%m-%dT%H:%M:%S')
            data = MonitoringEvents(
                Identifier = item["identifier"],
                Description = item["description"],
                Code = item["code"],
                OccurredOn = occured_on,
                SiteName = item["site"]["name"],
                ZorgName = item["zorg"]["name"],
                PollTime = poll_time
            )
            db_connection.add(data)
        
    # Save all collected data to the database
    db_connection.commit()

### PURGE OLD RECORDS ###
def purgeOldRecords (purge_time, poll_time, class_name):
    # Get records older than purge date
    results = db_connection\
        .query(class_name)\
        .filter(class_name.PollTime < purge_time)

    # For each record found delete it
    for item in results:
        db_connection.delete(item)

    # Commit deleted records
    db_connection.commit()
    
poll_interval_seconds = int(os.getenv("poll_interval_minutes")) * 60
while True:
    poll_time = datetime.utcnow()
    purge_time = poll_time - timedelta(days=int(os.getenv("purge_records_days")))

    print("Poll time " + str(poll_time) + "...")

    print("Getting apik token...")
    api_token = getAuthorizationToken()

    print("Getting data from Monitoring/Alerts...")
    getMonitoringAlerts(api_token, poll_time)

    print("Purging records from Monitoring/Alerts older than " + str(purge_time) + "...")
    purgeOldRecords (purge_time, poll_time, MonitoringAlerts)

    print("Getting data from Monitoring/Events...")
    getMonitoringEvents(api_token, poll_time)

    print("Purging records from Monitoring/Events older than " + str(purge_time) + "...")
    purgeOldRecords (purge_time, poll_time, MonitoringEvents)

    print("Sleeping for " + str(os.getenv("poll_interval_minutes")) + " minute(s)...")
    time.sleep(poll_interval_seconds)