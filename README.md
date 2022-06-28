Author: Evan Weis
Contact: weis.evan.c@gmail.com

Note: to use this script you must update the submissions_path, facts_path, and test_path to dorrespond with the location of your downloaded zip files...

SEC EDGAR (electronic data gathering, analysis, and retrival) system is an APi used to request public company filings. However programatic requets a rate limited, scraping is prohibited and the bilk download zip files filled with json are cumbersome.

The edgarDB.py script is a script used to build and deploy a sqlite3 database to query and analyze financial statements from public traded companies on the CBOE, OTC, NYSE, and Nasdaq exhanges.

Reports included in the databse are 10k and 10Q filings for all publicly traded companies insofar as EDGAR makes them available via the bulk download .zip files downloaded https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip and https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip

Contents of the reports include shares outstanding, market value (where aplicable) and the contents of the financial statements complaint with the generally accepted accounting principals (GAAP) reported to the SEC>

a json file with the description of the GAAP line items is included with this repository

Tables included in the datebase and associated schema are:
- companies
    cik, int primary key not null
    ticker, text not null
    sic, int not null
    description, text not null
    name, text not null
    exchange, text

Description:

    - cik: the central index key is a unique number assigned by the sec for companies to submit filings

    - ticker: a unique sting of letters used to identify a publicly traded company on a stock exchange

    - sic: Standard Industrial Classification Code is used to categorize industries that companies belong to based on business activities

    - description: is the text description of the sic code

    - name: is the name of the company

    - exchange: is the primary exhange the company is traded on i.e. NYSE

more to come...