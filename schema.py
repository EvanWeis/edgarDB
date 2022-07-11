# text strings for table schemas

company_schema = """
                    cik TEXT PRIMARY KEY NOT NULL,
                    ticker TEXT NOT NULL,
                    name TEXT NOT NULL,
                    sic TEXT,
                    descprition TEXT,
                    exchange TEXT
                 """

filing_schema = """
                    accn TEXT PRIMARY KEY NOT NULL,
                    cik TEXT,
                    form TEXT NOT NULL,
                    filingDate DATE,
                    reportDate DATE
                """

report_10K_schema = """
                        accn TEXT PRIMARY KEY NOT NULL,
                        report TEXT,
                        CommonStockSharesOutstanding INT,
                        CashAndEquivalent INT,
                        CurrentAssets INT,
                        Assets INT,
                        CurrentLiabilities INT,
                        LiabilitiesAndEquity INT,
                        NetIncome INT
                    """

report_10Q_schema = """
                        accn INT PRIMARY KEY NOT NULL,
                        outstanding_shares INT,
                    """
