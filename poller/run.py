### IMPORT REQUIRED PYTHON MODULES ###
import json, requests, time, datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm.exc import NoResultFound
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
    Identifier = Column(String, unique=False, nullable=False)
    Type = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    CollectionTime = Column(String, unique=False, nullable=False)
    PollTime = Column(String, unique=False, nullable=False)

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
def getMonitoringAlerts (api_token, poll_time):
    url = config.get("zerto_analytics_url") + "monitoring/alerts"
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
            print(results)
        except NoResultFound:
            # If a new alert save to database
            data = MonitoringAlerts(
                Identifier = item["identifier"],
                Type = item["type"],
                Description = item["description"],
                SiteName = item["site"]["name"],
                CollectionTime = (item["collectionTime"]),
                PollTime = poll_time
            )
            db_connection.add(data)
        
    # Save all collected data to the database
    db_connection.commit()

poll_interval_seconds = config.get("poll_interval_minutes") * 60
while True:
    poll_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    print("Poll time " + str(poll_time) + "...")

    print("Getting apik token...")
    api_token = getAuthorizationToken()

    print("Getting data from Monitoring/Alerts...")
    getMonitoringAlerts(api_token, poll_time)

    print("Sleeping for " + str(config.get("poll_interval_minutes")) + " minute(s)...")
    time.sleep(poll_interval_seconds)