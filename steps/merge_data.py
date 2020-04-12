import csv

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
counter = 0
with open('humidity_min.csv', 'r') as humidity_file:
    reader = csv.reader(humidity_file)
    for row in reader:
        print(row)
        if counter == 2:
            break
        counter = counter + 1

with open('temperature_min.csv', 'r') as temperature_file:
    temperature_reader = csv.reader(humidity_file)
    for temperature_row in temperature_reader:
        print(row)
        if counter == 2:
            break
        counter = counter + 1

humidity_file = csv.reader(open('humidity_min.csv'))

temperature_file = csv.reader(open('temperature_min.csv'))

merged_file = open('merge_dataset.csv', 'w')

with merged_file:
    writer = csv.writer(merged_file)
    writer.writerow(['DATA','TEMP','HUMIDITY'])
