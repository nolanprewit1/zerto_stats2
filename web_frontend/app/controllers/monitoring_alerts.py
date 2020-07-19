from app import app
from app import db_connection
from app.models import models_monitoring_alerts
from flask import render_template

# READ
@app.route("/monitoringAlerts")
def monitoring_alerts_index():
    # Get all records from the table
    results = db_connection\
        .query(models_monitoring_alerts.MonitoringAlerts)\
        .all()
    return render_template("monitoringAlerts/index.html", results=results)