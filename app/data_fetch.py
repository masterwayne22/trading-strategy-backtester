import yfinance as yf
import pandas as pd

def get_price_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Download daily price data for a symbol between start and end dates.
    Dates should be 'YYYY-MM-DD' strings.
    """
    data = yf.download(
        tickers=symbol,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if data is None or data.empty:
        raise ValueError("No data returned. Check symbol or dates.")

    data = data[["Close"]].copy()
    data.reset_index(inplace=True)
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
    return data

