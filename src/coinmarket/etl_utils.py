'''
ETL utils
'''
import os.path
import csv

def read_csv(csv_file):
    '''Get whole csv file'''
    table = []
    if not os.path.exists(csv_file):
        return table
    with open(csv_file, 'r') as inf:
        reader = csv.reader(inf)
        for row in reader:
            table.append(row)
    return table

def replace_csv_file(table, csv_file):
    '''Save whole data into csv file'''
    with open(csv_file, 'w', newline='') as out:
        csv_out = csv.writer(out)
        for row in table:
            csv_out.writerow(row)
    

def append_info(data, csv_file):
    '''Extract info and save'''

    with open(csv_file, 'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(data)

def append_tuples(d_tuple, csv_file):
    '''Extract info and save'''
    data = []
    data.append(d_tuple)

    with open(csv_file, 'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerows(data)

def sort_by(query, field):
    '''Sort info by field'''
    return sorted([e for e in query], key=lambda e: e[field], reverse=True)
