#! /usr/bin/env/python3
# script to translate the SECs Edgar json files to a local sqlite3 db
# this script requiers a local copy of the SEC filings in bulk, links below...
# cik to ticker flat file: https://www.sec.gov/files/company_tickers.json
# company submissions: https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip 
# company facts: https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip
# the file sizes are large and may take a while to download, approximately 5.69 Gb and 13 Gb respectively.

import os, sqlite3
from json import load
from schema import *
from sqlite3 import Error

test_path = "C:\\Users\\weise\\Documents\\Projects\\edgarDB\\edgar_sample\\"
submissions_path = "C://Users//weise//Desktop//EDGAR//submissions//"
facts_path = "C://Users//weise//Desktop//EDGAR//companyfacts//"

def create_db(db_name: str = 'edgar.db') -> None:
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_company_table(db_name: str = 'edgar.db', table_name: str = 'companies') -> None:

    #build file paths
    files = next(os.walk(submissions_path), (None, None, []))[2]
    files_path = [submissions_path + file for file in files if len(file) == 18]

    pc_values = []

    for p in files_path:
        with open(p, 'rb') as f:
            data = load(f)
            
            if not data['exchanges'] == []:
                n_zero = 10 - len(data['cik'])
                zs = n_zero * '0'
                cik =  zs + data['cik']
                values = (
                            int(cik),
                            data['tickers'][0],
                            int(data['sic']),
                            data['sicDescription'],
                            data['name'],
                            data['exchanges'][0]
                         )
                pc_values.append(values)

    try: 

        conn = sqlite3.connect(db_name)
        conn.execute("DROP TABLE IF EXISTS {}".format(table_name))
        conn.execute("CREATE TABLE {} ({})".format(table_name, company_schema))
    
    except Error as e:
        print("Error Creating Table")
        print(e)

    try:

        conn.executemany("INSERT INTO {} VALUES ( ?, ?, ?, ?, ?, ? )".format(table_name), pc_values)
        conn.commit()

    except Error as e:
        print("Error building table row")
        print(e)

    finally:
        if conn:
            conn.close()
    

def create_filings_table():
    pass

def create_reports_10k():
    pass

def create_report_10Q():
    pass

def create_edgar_db() -> None:
    pass


def main():

    create_db()
    create_company_table()

if __name__=='__main__': main()