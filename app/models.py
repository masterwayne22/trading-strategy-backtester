from pydantic import BaseModel
from typing import Literal, List


class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    short_window: int
    long_window: int
    strategy_type: Literal["ma", "rsi"]


class Trade(BaseModel):
    date: str
    price: float
    side: str  # "BUY" or "SELL"


class BacktestResponse(BaseModel):
    final_value: float
    total_return: float
    annualized_return: float
    annualized_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    trades: List[Trade]
    equity_curve: List[float]
    dates: List[str]



