import pymysql
import csv
from datetime import datetime

# Open database connection
db = pymysql.connect("localhost","root","admin","admin" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

csv_data = csv.reader(open('merge_dataset.csv', 'r'))
next(csv_data)
for row in csv_data:
    measure_date = datetime.strptime(row[0], "%d/%m/%Y %H:%M")
    print(measure_date)
    cursor.execute('INSERT INTO historical_data(measure_date,temperature, humidity) VALUES(%s, %s, %s)', (measure_date,row[1],row[2]))

db.commit()
# disconnect from server
db.close()