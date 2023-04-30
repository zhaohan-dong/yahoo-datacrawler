# Yahoo Finance/Webull Package for Intraday data/Trading

Note: work in progress.

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
`webull_client` extends `webull`. It makes it easier to authenticate user and create more complex orders currently
not supported by Webull, such as immediate or cancel. However it might not be possible to place hidden or all or none orders.
