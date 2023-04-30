import pandas as pd

def df_to_parquet(self, df: pd.DataFrame, path: str, engine: str = "pyarrow", compression: str = "gzip") -> bytes | None:
    return df.to_parquet(path=path, engine=engine, compression=compression)

def read_parquet(path: str, engine: str="pyarrow") -> pd.DataFrame:
    return pd.read_parquet(path, engine=engine, dtype_backend="pyarrow")