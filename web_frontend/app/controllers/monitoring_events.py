from app import app
from app import db_connection
from app.models.models_monitoring_events import MonitoringEvents
from flask import render_template

# READ
@app.route("/monitoringEvents")
def monitoring_events_index():
    # Get all records from the table
    results = db_connection\
        .query(MonitoringEvents)\
        .all()
    return render_template("monitoringEvents/index.html", results=results)