import yfinance as yf
import datetime


def quote(ticker: str):
    """
    Given a ticker, return last quote
    :param ticker: Ticker
    :return: Regular market price, post market bid price, ask price, bid size, ask size, quote access datetime
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    if info["marketState"] == "Closed":
        return info["postMarketPrice"], info["bid"], info["ask"], info["bidSize"], info["askSize"], datetime.datetime.now(tz=datetime.timezone.utc)

    return info["regularMarketPrice"], info["bid"], info["ask"], info["bidSize"], info["askSize"], datetime.datetime.now(tz=datetime.timezone.utc)