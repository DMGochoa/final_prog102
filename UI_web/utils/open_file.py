import csv
import os
import json



with open('./UI_web/data/example.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')