### IMPORT REQUIRED PYTHON MODULES ###
from flask import Flask, render_template, request, redirect, send_file
from project import app
from project.models import model_employees
from project import db_connection
from sqlalchemy import update

### DEFINE THE ROUTES ###
# CREATE
@app.route("/employees/create", methods=["GET", "POST"])
def employee_create():
    if request.method == "GET":
        return render_template("employees/create.html")
    elif request.method == "POST":
        # Save form data to the referenced object
        data = model_employees.Employees(
            firstName = request.form['firstName'],
            lastName = request.form['lastName'],
            position = request.form['position']
        )
        # Save the data to the database
        db_connection.add(data)
        db_connection.commit()
        return redirect("/employees", code=302)
    else:
        return redirect("/employees", code=302)

# READ
@app.route("/employees")
def employees_index():
    # Get all records from the table
    results = db_connection\
        .query(model_employees.Employees)\
        .all()
    return render_template("employees/index.html", results=results)

@app.route("/employees/detail/<id>", methods=["GET"])
def employees_detail(id):
    # Get the record matching the records id number
    results = db_connection\
        .query(model_employees.Employees)\
        .filter(model_employees.Employees.id==id)
    return render_template("employees/detail.html", results=results)

# UPDATE
@app.route("/employees/update/<id>", methods=["GET", "POST"])
def employee_update(id):
    if request.method == "GET":
        # Get the record matching the records id number
        results = db_connection\
            .query(model_employees.Employees)\
            .filter(model_employees.Employees.id==id)
        return render_template("employees/update.html", results=results)
    elif request.method == "POST":
        # Get the record matching the records id number
        results = db_connection\
            .query(model_employees.Employees)\
            .get(id)
        # Update record with form data
        results.firstName = request.form['firstName']
        results.lastName = request.form['lastName']
        results.position = request.form['position']
        # Save the data to the database
        db_connection.commit()
        return redirect("/", code=302)
    else:
        return redirect("/", code=302)

# DELETE
@app.route("/employees/delete/<id>", methods=["GET", "POST"])
def employee_delete(id):
    if request.method == "GET":
        # Get the record matching the records id number
        results = db_connection\
            .query(model_employees.Employees)\
            .filter(model_employees.Employees.id==id)
        return render_template("employees/delete.html", results=results)
    elif request.method == "POST":
        # Get the record matching the records id number
        results = db_connection\
            .query(model_employees.Employees)\
            .get(id)
        # Delete the record from the database
        db_connection.delete(results)
        db_connection.commit()
        return redirect("/", code=302)
    else:
        return redirect("/", code=302)