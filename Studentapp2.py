from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

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


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.google.com')


@app.route("/addstud", methods=['POST'])
def AddStud():
    Student_Id = request.form['Student_Id']
    Fname = request.form['Fname']
    Lname = request.form['Lname']
    Course_Name = request.form['Course_Name']
    YearofStudy = request.form['YearofStudy']
    student_image = request.files['student_image']

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = conn.cursor()

    if student_image.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (Student_Id, Fname, Lname, Course_Name, YearofStudy))
        conn.commit()
        student_name = "" + Fname + " " + Lname
        # Uploading image file in S3 #
        image_file = "Student-Id-" + str(Student_Id) + "_image"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(dbbucket).put_object(Key=image_file, Body=student_image)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=dbbucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
               	dbbucket,
                image_file)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddStudOutput.html', name=student_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
