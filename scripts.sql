-- SQLite3 Script to identify companies with highest "Gross Profitability Premium" as compared to book value 
-- based on Novy-Marx 2012, "The Other Side of Value: The Gross Profitability Premium"
-- http://rnm.simon.rochester.edu/research/OSoV.pdf


-- Count Companies, Distinct SIC in database
SELECT COUNT(name), COUNT(DISTINCT(sic)) 
FROM companies
;

-- Select All Distinct SIC and descriptions,
-- Count Companies in each SIC order largest SIC group first
SELECT DISTINCT(sic), descprition AS "Description", COUNT(name)
FROM companies

GROUP BY sic

ORDER BY COUNT(name) DESC
;

-- Calculate Average Gross Profitability by sector accross all years
-- Limit to companies with assets greater than $200,000
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

-- Calculate Median Gross Profitability by sector accross all years
-- Limit to compaines with assets greater than $200,000
-- Compare to Average accross all years

