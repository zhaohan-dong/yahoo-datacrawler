# Wrapper class to download data from Yahoo Finance using yfinance package
import pytz
import yfinance as yf
import pandas as pd
import datetime
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
                   start: str = None,
                   end: str = None,
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

        df = utils.pivot_price_df_by_ticker(df)

        df = utils.market_open_close(df)

        return df

    # Get options data for all available future dates at the moment
    def options_data(self):

        options_df = pd.DataFrame()  # create an empty DataFrame to store options data

        for ticker in self.__tickers:

            ticker_options_df = pd.DataFrame()
            expiration_dates = yf.Ticker(ticker).options

            for expiration_date in expiration_dates:
                option_chain = yf.Ticker(ticker).option_chain(
                    date=expiration_date)  # get the option chain for the ticker
                call_options = option_chain.calls  # get call options data
                put_options = option_chain.puts  # get put options data
                ticker_options_df = pd.concat(
                    [ticker_options_df, call_options, put_options])  # concatenate call and put options data
                ticker_options_df["accessTime"] = datetime.datetime.now(tz=pytz.timezone("America/New_York"))
                ticker_options_df["ticker"] = ticker

            options_df = pd.concat([options_df, ticker_options_df])

        return options_df
