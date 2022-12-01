import mysql.connector
import webbrowser
from pymysql import connections
from config import *

conn = connections.Connection(
    host=dbhost,
    port=3306,
    user=dbuser,
    password=dbpassword,
    db=database)

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
<title>Student Details</title>
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
webbrowser.open(filename)
cursor.close()
#fd
