import datetime
import pytz

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


def df_to_exchange_tz(df: pd.DataFrame, market: str) -> pd.DataFrame:
    # Get Exchange timezone
    exchange_tz = get_exchange_tz(market)

    # If dataframe is timezone naive
    if df["Datetime"].dt.tz is None:
        df["Datetime"] = df["Datetime"].dt.tz_localize(exchange_tz)

    # If dataframe is timezone aware
    elif df["Datetime"].dt.tz != get_exchange_tz(market):
        df["Datetime"] = df["Datetime"].dt.tz_convert(exchange_tz)

    return df


def market_open_close(df: pd.DataFrame, market: str = "US") -> pd.DataFrame:
    if market == "US":
        # Change dataframe's timezone to market's
        df = df_to_exchange_tz(df, market)
        df["Market"] = df["Datetime"].apply(lambda x: "Closed" if x.time() < datetime.time(hour=9, minute=30) or
                                                                  x.time() > datetime.time(hour=16) else "Open")
    else:
        print("Market not supported yet.")
        df["Market"] = None
        return df
    return df