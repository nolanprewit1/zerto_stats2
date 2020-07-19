from app import app
from app import db_connection
from app.models.models_monitoring_alerts import MonitoringAlerts
from flask import render_template

# READ
@app.route("/monitoringAlerts")
def monitoring_alerts_index():
    # Get all records from the table
    results = db_connection\
        .query(MonitoringAlerts)\
        .all()
    return render_template("monitoringAlerts/index.html", results=results)