import datetime
import pytz

import pandas as pd


def pivot_price_df_by_ticker(df: pd.DataFrame) -> pd.DataFrame:
    """
    The downloaded data is in a dataframe with two levels of column labels
    One level is the tickers, and the other is Open, Close, etc.
    We'll flatten it here
    :param df: Price dataframe downloaded from yfinance, with two levels of columns
    :return:
    """
    df = df.rename_axis(columns=('Ticker', None)).stack(0).reset_index().explode('Datetime')
    return df


def get_exchange_tz(market: str) -> datetime.tzinfo:
    """
    Get timezone given exchange's country
    :param market: Country of the Exchange
    :return:
    """

    match market:
        case "US":
            exchange_tz = pytz.timezone("America/New_York")
        case "UK":
            exchange_tz = pytz.timezone("Europe/London")
        case "Japan":
            exchange_tz = pytz.timezone("Asia/Tokyo")
        case "China":
            exchange_tz = pytz.timezone("Asia/Shanghai")
        case "Hong_Kong":
            exchange_tz = pytz.timezone("Asia/Hong_Kong")
        case "Canada":
            exchange_tz = pytz.timezone("America/Toronto")
        case "France":
            exchange_tz = pytz.timezone("Europe/Paris")
        case "Germany":
            exchange_tz = pytz.timezone("Europe/Berlin")
        case _:
            print("Market not supported yet, returning UTC")
            return pytz.UTC

    return exchange_tz


def market_open_close(df: pd.DataFrame, market: str = "US") -> pd.DataFrame:
    # Get exchange's timezone
    exchange_tz = get_exchange_tz(market)

    if market == "US":
        df["Market"] = df["Datetime"].dt.tz_localize(exchange_tz) \
            .apply(lambda x: "Closed" if x.time() < datetime.time(hour=9, minute=30) or
                                         x.time() > datetime.time(hour=16) else "Open")
    else:
        print("Market not supported yet.")
        df["Market"] = None
        return df
    return df
