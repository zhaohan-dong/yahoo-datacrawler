# Yahoo Finance/Webull Package for Data/Trading

This repo has two modules:
- yahoo_finance_data
- webull_client

`yahoo_finance_data` extends `yfinance` package and make it easier to get multiple-ticker intraday price data.
It also provides the ability to store data in the parquet format with the following structure.
```
./saved_data
├── AAPL
│   ├── AAPL-2023-04-24.parquet
│   ├── AAPL-2023-04-25.parquet
│   ├── AAPL-2023-04-26.parquet
│   ├── AAPL-2023-04-27.parquet
│   └── AAPL-2023-04-28.parquet
└── TSM
    └── TSM-2023-04-24.parquet
    └── TSM-2023-04-25.parquet
    └── TSM-2023-04-26.parquet
    └── TSM-2023-04-27.parquet
    └── TSM-2023-04-28.parquet
```
