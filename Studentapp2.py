from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = bucket
region = region

conn = connections.Connection(
    host=host,
    port=3306,
    user=user,
    password=password,
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


@app.route("/addemp", methods=['POST'])
def AddStud():
    Student_Id = request.form['Student_Id']
    Fname = request.form['Fname']
    Lname = request.form['Lname']
    Course_Name = request.form['Course_Name']
    YearofStudy = request.form['YearofStudy']
    stud_image_file = request.files['stud_image_file']

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = conn.cursor()

    if stud_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (Student_Id, Fname, Lname, Course, YearofStudy))
        conn.commit()
        Stud_name = "" + Fname + " " + Lname
        # Uplaod image file in S3 #
        stud_image_file_name_in_s3 = "Student-Id-" + str(Student_Id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(bucket).put_object(Key=stud_image_file_name_in_s3, Body=stud_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
               	bucket,
                studimage_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddStudOutput.html', name=Stud_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
