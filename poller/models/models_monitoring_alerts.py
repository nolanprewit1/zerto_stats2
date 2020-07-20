from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Create obect that related to database table
class MonitoringAlerts(declarative_base()):
    __tablename__ = "monitoring_alerts"
    Id = Column(Integer, primary_key=True)
    Identifier = Column(String, unique=False, nullable=False)
    Type = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    CollectionTime = Column(DateTime, unique=False, nullable=False)
    PollTime = Column(DateTime, unique=False, nullable=False)