from app import app
from app import db_connection
from app.models import models_monitoring_alerts
from flask import redirect, url_for

# READ
@app.route('/')
def index():
    return redirect(url_for('monitoring_alerts_index'))