import csv

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

rows_to_add = 500
added_rows = 0
index = 0

merged_file = open('merge_dataset.csv', 'w')
with merged_file:
    writer = csv.writer(merged_file)
    writer.writerow(['DATE','TEMP','HUMIDITY'])

    with open('humidity_min.csv', 'r') as humidity_file:
        with open('temperature_min.csv', 'r') as temperature_file:

            humidity_reader = csv.reader(humidity_file)
            temperature_reader = csv.reader(temperature_file)

            while index < rows_to_add:
                humidity_row = next(humidity_reader)
                temperature_row = next(temperature_reader)
                
                print(index)
                index = index + 1
                print([humidity_row[0],temperature_row[3],humidity_row[3]])
                if is_number(humidity_row[3]) and is_number(temperature_row[3]):
                    writer.writerow([humidity_row[0],temperature_row[3],humidity_row[3]])
                    added_rows = added_rows + 1
                if(added_rows == rows_to_add or index == rows_to_add):
                    break
            


