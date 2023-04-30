# Wrapper class to download data from Yahoo Finance using yfinance package
from typing import Any
import pytz
import yfinance as yf
import pandas as pd
import datetime
from . import utils
from . import quote


class YahooBatchLoader:

    __tickers: list[str]
    __prices: pd.DataFrame

    def __init__(self, tickers: list[str]):
        self.__tickers = tickers

    def set_tickers(self, tickers: list[str]) -> None:
        self.__tickers = tickers
        return None

    def get_tickers(self) -> list[str]:
        return self.__tickers

    def get_prices(self,
                   start: Any = None,
                   end: Any = None,
                   period: str = "max",
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

        # Download ticker data from yahoo
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

        df = utils.rename_index_datetime(df)

        df = utils.pivot_price_df_by_ticker(df, self.__tickers)

        df = utils.market_open_close(df, market="US")

        self.__prices = df

        return df

    def last_price(self):
        tickers = yf.Tickers(self.__tickers)
        print(tickers.tickers.info)

    # Get options data for all available future dates at the moment
    def options_data(self) -> pd.DataFrame:

        options_df = pd.DataFrame()  # create an empty DataFrame to store options data

        for ticker in self.__tickers:

            ticker_options_df = pd.DataFrame()

            # Get a list of expiration dates
            expiration_dates = yf.Ticker(ticker).options

            # yfinance does not provide a way to get all expiration date options price, so we have to query one by one
            for expiration_date in expiration_dates:
                option_chain = yf.Ticker(ticker).option_chain(
                    date=expiration_date)  # get the option chain for the ticker
                call_options = option_chain.calls  # get call options data
                put_options = option_chain.puts  # get put options data
                ticker_options_df = pd.concat(
                    [ticker_options_df, call_options, put_options])  # concatenate call and put options data
                ticker_options_df["accessTime"] = datetime.datetime.now(tz=pytz.UTC)
                ticker_options_df["ticker"] = ticker

            options_df = pd.concat([options_df, ticker_options_df])

        return options_df

    def price_to_parquet(self, path: str, engine: str="pyarrow", compression: str="gzip"):
        self.__prices.to_parquet(path=path, engine=engine, compression=compression)
        return None