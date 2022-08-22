#! /usr/bin/env/python3

# script to create and build an SQLlite3 DB for the Russell 2000 index
# for analysis or use with edgar.db

import sqlite3
import csv
from edgartodb import create_db
from schema import r2k_schema
from sqlite3 import Error



russell_2k = "C:\\Users\\weise\\Documents\\GitHub\\edgarDB\\assets\\russell_2000.csv"


def build_r2k_table(db_name, table_name):
    with open(russell_2k) as f:
        reader = csv.reader(f)

    try: 
        conn = sqlite3.connect(db_name)
        conn.execute("DROP TABLE IF EXISTS {}".format(table_name))
        conn.execute("CREATE TABLE {} ({})".format(table_name, r2k_schema))  

    except Error as e:
        print(e)  


def main():
    #create_db(db_name = "russel2k.db")
    build_r2k_table()

if __name__ == "__main__": main()