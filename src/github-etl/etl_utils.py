'''
ETL utils
'''
import os.path
import csv


def append_info(repository, csv_file, header):
    '''Extract info and save'''
    data = []
    if not os.path.exists(csv_file):
        data.insert(0, header)

    data.append(repository)

    with open(csv_file, 'a', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerows(data)
    #print(repository)

def sort_by(query, field):
    '''Sort info by field'''
    return sorted([e for e in query], key=lambda e: e[field], reverse=True)
