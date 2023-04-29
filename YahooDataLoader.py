# Wrapper class to download data from Yahoo Finance using yfinance package

import yfinance as yf
import pandas as pd
import datetime
import zoneinfo
import utils


class YahooDataLoader:

    __tickers: list[str]

    def __init__(self, tickers: list[str]):
        self.__tickers = tickers

    def set_tickers(self, tickers: list[str]):
        self.__tickers = tickers

    def get_tickers(self):
        return self.__tickers

    def get_prices(self,
                   start: str=None,
                   end: str=None,
                   period: str = "5d",
                   interval: str = "1m",
                   prepost: bool = True,
                   keepna: bool = False) -> pd.DataFrame:

        """
         Method to load previous trading session's data
         (Should run after 8pm Eastern Time / end of post-market session)
        :param start: Start date for historical data query
        :param end: End date for historical data query
        :param period: Period of query, default to 5 days (can be set to max in conjunction with start/end)
        :param interval: Resolution interval for data, smallest is 1 minute, but can only get the last 7 days
        :param prepost: Pre-/Post-market data
        :param keepna: Keep NA entries
        :return: A pandas dataframe of prices
        """

        df = yf.download(tickers=self.__tickers,
                                       start=start,
                                       end=end,
                                       period=period,
                                       interval=interval,
                                       prepost=prepost,
                                       actions=True,
                                       progress=False,
                                       group_by="ticker",
                                       keepna=keepna)

        df = df.rename_axis(columns=('Ticker',None)).stack(0).reset_index().explode('Datetime')
        df.loc[(df.Datetime.dt.time < datetime.time(hour=9, minute=30)) |
               (df.Datetime.dt.time > datetime.time(hour=16)), "Market"] = "Closed"
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
