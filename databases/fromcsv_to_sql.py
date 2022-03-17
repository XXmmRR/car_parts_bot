import csv
from db import Session
from db import CreateBaseCars

file = 'base_cars_full.csv'


def add_to_db(filename):
    session = Session
    File = open(file, 'r')
    reader = csv.reader(File)
    for i in reader:
        cars = CreateBaseCars()
        session.add(cars)


if __name__ == '__main__':
    add_to_db(file)
