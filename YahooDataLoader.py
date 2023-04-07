# Wrapper class to download data from Yahoo Finance using yfinance package

import yfinance as yf
import pandas as pd
import datetime
import zoneinfo


class YahooDataLoader:
    ticker: str

    def __init__(self, ticker):
        self.ticker = str.upper(ticker)
        self.yf_ticker: yf.Ticker = yf.Ticker(self.ticker)

    # Method to load previous trading session's data
    # (Should run after 8pm Eastern Time / end of post-market session)
    def session_price(self,
                      period: str = "1d",
                      interval: str = "1m",
                      prepost: bool = True,
                      keepna: bool = False) -> pd.DataFrame:
        df: pd.DataFrame = self.yf_ticker.history(period=period,
                                                  interval=interval,
                                                  prepost=prepost,
                                                  keepna=keepna)
        df["Ticker"] = self.ticker
        df.loc[(df.index.time < datetime.time(hour=9, minute=30)) |
               (df.index.time > datetime.time(hour=16)), "Market"] = "Closed"
        df.loc[pd.isnull(df["Market"]), "Market"] = "Open"
        return df

    # Get options data for all available future dates at the moment
    def options_data(self):
        expiration_dates: tuple = self.yf_ticker.options
        df_options = pd.DataFrame()

        for date in expiration_dates:
            calls = pd.concat([self.yf_ticker.option_chain(date=date).calls])
            calls["Type"] = "Call"

            puts = pd.concat([self.yf_ticker.option_chain(date=date).puts])
            puts["Type"] = "Put"

            opt = pd.concat([calls, puts])
            opt["expirationDate"] = date
            opt["accessTime"] = datetime.datetime.now(tz=zoneinfo.ZoneInfo("America/New_York"))
            df_options = pd.concat([df_options, opt])

        return df_options
