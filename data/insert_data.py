import pymysql
import csv

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
    print(row[1])
    cursor.execute('INSERT INTO historical_data(measure_date,temperature, humidity) VALUES(%s, %s, %s)', ('2019-03-10 02:55:05',row[1],row[2]))

db.commit()
# disconnect from server
db.close()