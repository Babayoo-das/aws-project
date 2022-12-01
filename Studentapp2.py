from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *
import webbrowser

app = Flask(__name__)

bucket = dbbucket
region = dbregion

conn = connections.Connection(
    host=dbhost,
    port=3306,
    user=dbuser,
    password=dbpassword,
    db=database

)
output = {}
table = 'student'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddStud.html')


@app.route("/about", methods=['GET'])
def about():
    select_sql = "select * from student"
    cursor = conn.cursor()
    cursor.execute(select_sql)
    result = cursor.fetchall()
    p = []
    
    tbl =  "<tr><td>Student ID</td><td>First Name</td><td>Last Name</td><td>Course Name</td><td>Year of Study</td></tr>"
    p.append(tbl)
    for row in result:
        a = "<tr><td>%s</td>"%row[0]
        p.append(a)
        b = "<td>%s</td>"%row[1]
        p.append(b)
        c = "<td>%s</td>"%row[2]
        p.append(c)
        d = "<td>%s</td></tr>"%row[3]
        p.append(d)
        e = "<td>%s</td></tr>"%row[4]
        p.append(e)
        
    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
    <title>Python Webbrowser</title>
    </head>
    <body>
    <table>%s</table>
    </body>
    </html>'''%(p)
        
    filename = 'getstudents.html'
    def main(contents, filename):
        output = open(filename,"w")
        output.write(contents)
        output.close()
    main(contents, filename)
    return webbrowser.open(filename)
    
    cursor.close()


@app.route("/addstud", methods=['POST'])
def AddStud():
    Student_Id = request.form['Student_Id']
    Fname = request.form['Fname']
    Lname = request.form['Lname']
    Course_Name = request.form['Course_Name']
    YearofStudy = request.form['YearofStudy']

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = conn.cursor()

    try:

        cursor.execute(insert_sql, (Student_Id, Fname, Lname, Course_Name, YearofStudy))
        conn.commit()
        student_name = "" + Fname + " " + Lname
        
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(dbbucket).put_object(Key=Student_Id, Body=Student_Id)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=dbbucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
               	dbbucket,
                Student_Id)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddStudOutput.html', name=student_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
