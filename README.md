# EDGAR SEC Database

The intent of this database is to enhance the speed and efficiency of fundimental analysis used by some investors to identify potential investment opportunbities.

**Note:** to use this script you must update the submissions_path, facts_path, and test_path to correspond with the location of your downloaded zip files...

SEC EDGAR (electronic data gathering, analysis, and retrival) system is an APi used to request public company filings. However programatic requets a rate limited, scraping is prohibited and the bilk download zip files filled with json are cumbersome.

The edgarDB.py script is a script used to build and deploy a sqlite3 database to query and analyze financial statements from public traded companies on the CBOE, OTC, NYSE, and Nasdaq exhanges.

Reports included in the databse are 10k and 10Q filings for all publicly traded companies insofar as EDGAR makes them available via the bulk download .zip files downloaded [here](https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip "Submissions zip") and [here](https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip "Company Facts zip")

Contents of the reports include shares outstanding, market value (where aplicable) and the contents of the financial statements complaint with the generally accepted accounting principals (GAAP) reported to the SEC.

Tables included in the datebase and associated schema are

**companies:**

    cik TEXT PRIMARY KEY NOT NULL,
    ticker TEXT NOT NULL,
    name TEXT NOT NULL,
    sic TEXT,
    description TEXT,
    exchange TEXT

Description:

    - cik: the central index key is a unique number assigned by the sec for companies to submit filings

    - ticker: a unique sting of letters used to identify a publicly traded company on a stock exchange

    - sic: Standard Industrial Classification Code is used to categorize industries that companies belong to based on business activities

    - description: is the text description of the sic code

    - name: is the name of the company

    - exchange: is the primary exhange the company is traded on i.e. NYSE

**filings**

    accn TEXT PRIMARY KEY NOT NULL,
    cik TEXT,
    form TEXT NOT NULL,
    filingDate DATE,
    reportDate DATE,

Description:

    - accn: accession number for specific filings organizing the line items in the financials

    - cik: serves as foreign key

    - form: either 10-K or 10-Q

    - filingDate: date form was filied with SEC

    - reportDate: fiscal period end report is referencing

**annualReports and quarterlyReports**
*table schema are the same, difference is in the report contents, 10-K and 10-Q respectively*

*as of this stage of development the tables are incomplete covering only a portion of the balance sheet*

    accn TEXT PRIMARY KEY NOT NULL,
    report TEXT,
    CommonStockSharesOutstanding INT,
    CashAndEquivalent INT,
    CurrentAssets INT,
    Assets INT,
    CurrentLiabilities INT,
    LiabilitiesAndEquity INT,
    NetIncome INT

Description of this table should be self explainatory at this point with the financial components being somewhat intuitive, I wont belabor the point by describing them further.

Future development includes plans to include a json file with a complete description of the GAAP in the repo.

## Creating the Database

This process requires the `facts_path` and `submissions_path` to be updated to reference the location of the directory in which the json files live. 

The output is an sqlite3 databse in the directory where the script is run.

**Usage:**

```python
create_company_table()
create_filings_table()
create_reports_table('10-Q', 'quarterlyReports')
create_reports_table('10-K', 'annualReports')
```


**Sample usage of sqlite3:**

```SQL
SELECT sic AS "SIC",
descprition AS "Description",
COUNT(name) AS "Compaines Included",

ROUND(AVG(NetIncome), 0) AS "Avg Profit",
ROUND(AVG(Assets), 0) AS "Avg Assets",

ROUND(AVG(CAST(NetIncome AS float)/CAST(Assets AS float)), 4) AS "Avg Gross Profitability"

FROM Companies AS c
JOIN filings AS f
ON c.cik = f.cik
JOIN annualReports AS a
ON f.accn = a.accn

WHERE Assets > 200000 AND strftime('%Y', f.reportDate) IN ('2018', '2019', '2020', '2021')

GROUP BY sic

ORDER BY AVG(CAST(NetIncome AS float)/CAST(Assets AS float)) DESC
LIMIT 15
;
```

Outputs of top SICs with the heighest average gross profitability ratio for the years 2018-2021


**Note:**

Due to inconsistencies in filing format from accross companies and years the `INSERT` failure rate is still quite high. Improvements are ongoing.


