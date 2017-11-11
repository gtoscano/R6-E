'''
ETL utils
'''
import os.path
import csv


def append_info(data, csv_file):
    '''Extract info and save'''

    with open(csv_file, 'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow([data])
    
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
