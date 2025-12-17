import os 
import csv 
from datetime import date
from flask import Flask, render_template, request, redirect,url_for
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/service")
def service():
   return render_template("service.html")

@app.route("/admin-login", methods = ["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        admin_code = request.form.get("admin_code")
        password = request.form.get("password")
        if admin_code == "AD001" and password == "3421":
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid Admin Code or Password"
    return render_template("admin_login.html", error=error)
@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/employee-login", methods=["GET", "POST"])
def employee_login():
    error = None
    if request.method == "POST":
        emp_code = request.form.get("emp_code")
        password = request.form.get("password")
        with open("employees.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["emp_code"] == emp_code and row["password"] == password:
                    return redirect(url_for("employee_attendance"))
        error = "Invalid Employee Code or Password"
    return render_template("employee_login.html", error=error)
@app.route("/employee_dashboard")
def employee_dashboard():
    return render_template("employee_dashboard.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/employee-attendance", methods = ["GET", "POST"])
def employee_attendance():
    message = None
    if request.method == "POST":
        emp_code = request.form.get("emp_code")
        attendance_date = request.form.get("date")
        shift = request.form.get("shift")
        status = request.form.get("status")
        
        with open("attendance.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([emp_code, attendance_date, shift, status])
        message = "Attendance submitted successfully"
    return render_template("employee_attendance.html", message=message)
@app.route("/admin-attendance")
def admin_attendance():
    records = []
    try:
        with open("attendance.csv", "r") as file:
            reader = csv.reader(file)
            records = list(reader)
    except:
        records = []
    return render_template("admin_attendance.html", records=records)
@app.route("/change-password", methods = ["GET", "POST"])
def change_password():
    message = None
    if request.method == "POST":
        emp_code = request.form.get("emp_code")
        new_password = request.form.get("new_password")
        
        rows = []
        updated = False
        
        with open("employees.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["emp_code"] == emp_code:
                   row["password"] == new_password
                   updated = True
                rows.append(row)
        if updated:
            with open("employees.csv", "r")as file:
                writer = csv.DictReader(file, fieldnames=["emp_code", "password", "name"])
                writer.writeheader()
                writer.writerows(rows)
            message = "Password updated succesfully"
        else:
            message = "Employee not found"
    return render_template("change_password.html", message=message)
            
if __name__ == "__main__":
    app.run(debug=True) 
