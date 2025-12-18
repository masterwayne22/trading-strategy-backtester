import pandas as pd
import numpy as np


def compute_metrics(equity_curve, initial_capital=100000.0, periods_per_year=252):
    equity = np.array(equity_curve, dtype=float)
    if len(equity) < 2:
        return 0.0, 0.0, 0.0, 0.0

    returns = equity[1:] / equity[:-1] - 1
    total_return = equity[-1] / initial_capital - 1

    avg_ret = returns.mean()
    vol = returns.std()

    if vol > 0:
        ann_return = (1 + avg_ret) ** periods_per_year - 1
        ann_vol = vol * np.sqrt(periods_per_year)
        sharpe = ann_return / ann_vol if ann_vol > 0 else 0.0
    else:
        ann_return = 0.0
        ann_vol = 0.0
        sharpe = 0.0

    return float(total_return), float(ann_return), float(ann_vol), float(sharpe)


def rsi_strategy(df, period=14, lower=30, upper=70):
    df = df.copy()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi

    df["signal"] = 0
    df.loc[df["rsi"] < lower, "signal"] = 1
    df.loc[df["rsi"] > upper, "signal"] = 0
    return df


def moving_average_backtest(
    df: pd.DataFrame,
    short_window: int,
    long_window: int,
    initial_capital: float = 100000.0,
    strategy_type: str = "ma",
):
    """
    Backtest with Moving Average or RSI strategy.
    df must have columns: Date (str), Close (float).
    """

    df = df.copy()
    df = df.reset_index(drop=True)

    if strategy_type == "ma":
        df["short_ma"] = df["Close"].rolling(window=short_window).mean()
        df["long_ma"] = df["Close"].rolling(window=long_window).mean()
        df["signal"] = 0
        df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1

    elif strategy_type == "rsi":
        df = rsi_strategy(df)

    else:
        raise ValueError(f"Unknown strategy_type: {strategy_type}")

    # yesterday's signal = today's position
    df["position"] = df["signal"].shift(1).fillna(0)

    df["return"] = df["Close"].pct_change().fillna(0)
    df["strategy_return"] = df["position"] * df["return"]

    df["equity_curve"] = (1 + df["strategy_return"]).cumprod() * initial_capital

    equity_values = df["equity_curve"].tolist()
    dates = df["Date"].astype(str).tolist()

    cummax = df["equity_curve"].cummax()
    drawdown = df["equity_curve"] / cummax - 1
    max_drawdown = float(drawdown.min())

    trades = []
    prev_pos = 0
    for _, row in df.iterrows():
        pos = int(row["position"])
        if pos != prev_pos:
            side = "BUY" if pos == 1 else "SELL"
            trades.append(
                {
                    "date": str(row["Date"]),
                    "price": float(row["Close"]),
                    "side": side,
                }
            )
        prev_pos = pos

    final_value = float(equity_values[-1])
    total_return, ann_ret, ann_vol, sharpe = compute_metrics(
        equity_values, initial_capital
    )

    return {
        "final_value": final_value,
        "total_return": float(total_return),
        "annualized_return": float(ann_ret),
        "annualized_volatility": float(ann_vol),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": max_drawdown,
        "trades": trades,
        "equity_curve": equity_values,
        "dates": dates,
    }


