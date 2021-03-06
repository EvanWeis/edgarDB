#! /usr/bin/env/python3
# script to translate the SECs Edgar json files to a local sqlite3 db
# this script requiers a local copy of the SEC filings in bulk, links below...
# cik to ticker flat file: https://www.sec.gov/files/company_tickers.json
# company submissions: https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip 
# company facts: https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip
# the file sizes are large and may take a while to download, approximately 5.69 Gb and 13 Gb respectively.

from itertools import zip_longest
import os, sqlite3
from json import load
from schema import *
from sqlite3 import Error

test_submissions_path = "C:\\Users\\weise\\Documents\\Projects\\edgarDB\\edgar_sample\\submissions\\"
test_filings_path = "C:\\Users\\weise\\Documents\\Projects\\edgarDB\\edgar_sample\\filings\\"
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
            
            if not data['exchanges'] == [] and not data == {}:
                n_zero = 10 - len(data['cik'])
                zs = n_zero * '0'
                cik =  zs + data['cik']
                values = (
                            cik,
                            data['tickers'][0],
                            data['name'],
                            data['sic'],
                            data['sicDescription'],
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
    

def create_filings_table(db_name: str = 'edgar.db', table_name: str = 'filings') -> None:

    files = next(os.walk(submissions_path), (None, None, []))[2]
    files_path = [submissions_path + file for file in files if len(file) == 18]

    pc_values = []
    uniq = []
    seen = set()
    for p in files_path:
        with open(p, 'rb') as f:
            data = load(f)
            
        if not data['exchanges'] == [] or not data == {}:

            index_map = []
            for m in range(0, len(data['filings']['recent']['form'])):
                if data['filings']['recent']['form'][m] in ['10-K', '10-Q']:
                    index_map.append(m)

        for i in index_map:
            n_zero = 10 - len(data['cik'])
            zs = n_zero * '0'
            cik =  zs + data['cik']
            if data['filings']['recent']['accessionNumber'][i] not in seen:
                uniq.append(data['filings']['recent']['accessionNumber'][i])
                seen.add(data['filings']['recent']['accessionNumber'][i])

                values = (
                    data['filings']['recent']['accessionNumber'][i],
                    cik,
                    data['filings']['recent']['form'][i],
                    data['filings']['recent']['filingDate'][i],
                    data['filings']['recent']['reportDate'][i]
                )
            
                pc_values.append(values)


    try:
            
        conn = sqlite3.connect(db_name)        
        conn.execute("DROP TABLE IF EXISTS {}".format(table_name))
        conn.execute("CREATE TABLE {} ({})".format(table_name, filing_schema))

    except Error as e:
        print('ERROR creating table')
        print(e)
        
    try:
        
        conn.executemany("INSERT INTO {} VALUES (?, ?, ?, ?, ?)".format(table_name), pc_values)
        conn.commit()

    except Error as e:
        print('ERROR updating table')
        print(e)

    finally:
        if conn:
            conn.close()
       

def create_reports_table(form: str, table_name: str, db_name: str = 'edgar.db') -> None:


    files = next(os.walk(facts_path), (None, None, []))[2]
    files_path = [facts_path + file for file in files if len(file) == 18]

    try:
                    
        conn = sqlite3.connect(db_name)        
        conn.execute("DROP TABLE IF EXISTS {}".format(table_name))
        conn.execute("CREATE TABLE {} ({})".format(table_name, report_10K_schema))

    except Error as e:
        print('ERROR creating table')
        print(e)

    for p in files_path:
        with open(p, 'rb') as f:
            data = load(f)

        try:
            trans = []
            accn = [
                data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][i]['accn']
                for i in 
                range(len(data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']))
                if 
                data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][i]['form'] == form
            ]
            try:
                cash = {
                    data['facts']['us-gaap']['CashAndCashEquivalentsAtCarryingValue']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['CashAndCashEquivalentsAtCarryingValue']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['CashAndCashEquivalentsAtCarryingValue']['units']['USD']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:
                shares = {
                    data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][i]['accn'] :
                    data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][i]['val']
                    for i in 
                    range(len(data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:      
                ac = {
                    data['facts']['us-gaap']['AssetsCurrent']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['AssetsCurrent']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['AssetsCurrent']['units']['USD']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:
                assets = {
                    data['facts']['us-gaap']['Assets']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['Assets']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['Assets']['units']['USD']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:
                lc = {
                    data['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:             
                le = {
                    data['facts']['us-gaap']['LiabilitiesAndStockholdersEquity']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['LiabilitiesAndStockholdersEquity']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['LiabilitiesAndStockholdersEquity']['units']['USD']))
                }
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass
            try:
                ni = {
                    data['facts']['us-gaap']['NetIncomeLoss']['units']['USD'][i]['accn'] :
                    data['facts']['us-gaap']['NetIncomeLoss']['units']['USD'][i]['val']
                    for i in 
                    range(len(data['facts']['us-gaap']['NetIncomeLoss']['units']['USD']))
                }     
            except KeyError as e:
                print("Warning, KeyError:", e, " is not a valid key")
                pass

            for k,a,b,c,d,e,f,g in zip_longest( assets.keys(),
                                                shares.values(),
                                                cash.values(),
                                                ac.values(),
                                                assets.values(),
                                                lc.values(),
                                                le.values(),
                                                ni.values()
                                                ):
                if k in accn:
                    vals = (k,form,a,b,c,d,e,f,g)
                    trans.append(vals)
            try:

                conn = sqlite3.connect(db_name)
                conn.executemany("INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name), trans)
                conn.commit()

            except Error as e:
                print('ERROR updating table')
                print(e)

            finally:
                if conn:
                    conn.close()
        except KeyError as e:
            print('No Key: ', e)
            pass

def main():
    
    #create_company_table()
    #create_filings_table()
    #create_reports_table('10-Q', 'quarterlyReports')
    pass

if __name__=='__main__': main()