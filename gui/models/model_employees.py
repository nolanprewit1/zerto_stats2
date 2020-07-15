from project import Base
from sqlalchemy import Column, String, Integer

# Create Employees ojbect with relates to the Employees table
class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    position = Column(String)