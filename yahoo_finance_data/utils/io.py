import pandas as pd
import os

def df_to_parquet(df: pd.DataFrame, root_dir: str, filename: str=None, engine: str = "pyarrow", compression: str = "gzip") -> bytes | None:
    # If no filename is given, we'll store parquet files in a directory tree with individual ticker/date
    if filename == None:
        dates = df["Datetime"].dt.date.unique()
        tickers = df["Ticker"].unique()
        for ticker in tickers:
            if not os.path.exists(os.path.join(root_dir, ticker)):
                os.makedirs(os.path.join(root_dir, ticker), exist_ok=False)
            for date in dates:
                write_df = df.loc[(df["Ticker"]==ticker) & (df["Datetime"].dt.date==date), :]
                write_df.to_parquet(path=os.path.join(root_dir, ticker, f"{ticker}-{date}.parquet"), engine=engine, compression=compression)
    else:
        return df.to_parquet(path=os.path.join(root_dir, filename), engine=engine, compression=compression)

def read_parquet(root_dir: str, tickers: str=None, start: str=None, end: str=None, filename: str=None, engine: str="pyarrow") -> pd.DataFrame:

    output_df = pd.DataFrame()

    # Read tickers
    if filename==None:
        if tickers==None:
            tickers = [ticker for ticker in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, ticker))]

        for ticker in tickers:
            output_df = pd.concat([output_df,
                                   pd.read_parquet(path=os.path.join(root_dir,))])



    return pd.read_parquet(path, engine=engine, dtype_backend="pyarrow")