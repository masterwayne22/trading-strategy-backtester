from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import BacktestRequest, BacktestResponse
from .data_fetch import get_price_data
from .strategy import moving_average_backtest

app = FastAPI(title="Trading Strategy Backtester MVP")

# Allow requests from browser (index.html)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/backtest", response_model=BacktestResponse)
def run_backtest(req: BacktestRequest):
    try:
        df = get_price_data(req.symbol, req.start_date, req.end_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if req.short_window >= req.long_window and req.strategy_type == "ma":
        # only enforce this rule for moving-average strategy
        raise HTTPException(
            status_code=400,
            detail="short_window must be less than long_window",
        )

    result = moving_average_backtest(
        df,
        req.short_window,
        req.long_window,
        strategy_type=req.strategy_type,
    )

    return result

