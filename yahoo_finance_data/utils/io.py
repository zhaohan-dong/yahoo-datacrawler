import pandas as pd

def df_to_parquet(self, df: pd.DataFrame, path: str, engine: str = "pyarrow", compression: str = "gzip"):
    df.to_parquet(path=path, engine=engine, compression=compression)
    return None