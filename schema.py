# text strings for table schemas

company_schema = """
                    cik INT PRIMARY KEY NOT NULL,
                    ticker TEXT NOT NULL,
                    name TEXT NOT NULL,
                    sic INT,
                    descprition TEXT,
                    exchange TEXT
                 """

filing_schema = """
                    accn INT PRIMARY KEY NOT NULL,
                    cik INT FOREIGN KEY NOT NULL,
                    end DATE,
                    fy TEXT,
                    fp TEXT,
                    form TEXT,
                    filing_date, DATE
                """

report_10K_schema = """
                        accn INT PRIMARY KEY NOT NULL,
                        outstanding_shares INT,
                        market_value INT,
                    """

report_10Q_schema = """
                        accn INT PRIMARY KEY NOT NULL,
                        outstanding_shares INT,
                    """
