from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Create obect that related to database table
class MonitoringEvents(declarative_base()):
    __tablename__ = "monitoring_events"
    Id = Column(Integer, primary_key=True)
    Identifier = Column(String, unique=False, nullable=False)
    Description = Column(String, unique=False, nullable=False)
    Code = Column(String, unique=False, nullable=False)
    OccurredOn = Column(DateTime, unique=False, nullable=False)
    SiteName = Column(String, unique=False, nullable=False)
    ZorgName = Column(String, unique=False, nullable=True)    
    PollTime = Column(DateTime, unique=False, nullable=False)