# Trading Strategy Backtester (FastAPI + JS)

Interactive web app to backtest **Moving Average** and **RSI** trading strategies on stocks (US + NSE) with performance metrics and an equity‑curve chart.

## Features

- FastAPI backend with a `/backtest` POST endpoint.
- Supports:
  - Moving Average crossover strategy (`strategy_type = "ma"`).
  - RSI strategy (`strategy_type = "rsi"`).
- Calculates:
  - Final portfolio value.
  - Total and annualized return.
  - Annualized volatility.
  - Sharpe ratio.
  - Max drawdown.
- Generates BUY/SELL trades and full equity curve.
- Frontend dashboard:
  - Stylish “trading terminal” UI.
  - Form for symbol, date range, short/long windows, strategy selection.
  - Trades table with entry/exit prices.
  - Equity curve line chart using Chart.js.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic  
- **Data & Analytics:** Pandas, NumPy, (e.g. yfinance for market data)  
- **Frontend:** HTML, CSS, Vanilla JavaScript, Chart.js  

## Getting Started

### 1. Clone the repo

git clone https://github.com/masterwayne22/trading-strategy-backtester.git
cd trading-strategy-backtester


### 2. Set up and install dependencies

python -m venv venv
venv\Scripts\activate # on Windows

source venv/bin/activate # on macOS / Linux
pip install -r requirements.txt



### 3. Run the FastAPI backend

uvicorn app.main:app --reload


Backend will be available at `http://127.0.0.1:8000`.

You can also open interactive docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`

### 4. Run the frontend

Open `index.html` in your browser (or serve it via any simple static file server).  
Make sure it points to `http://127.0.0.1:8000/backtest` for API calls.

## API

### `POST /backtest`

**Request body (JSON):**

{
"symbol": "AAPL",
"start_date": "2020-01-01",
"end_date": "2024-12-01",
"short_window": 50,
"long_window": 200,
"strategy_type": "ma"
}



`strategy_type` is `"ma"` for Moving Average or `"rsi"` for RSI.

**Response (simplified):**

{
"final_value": 153746.81,
"total_return": 0.5375,
"annualized_return": 0.1084,
"annualized_volatility": 0.1660,
"sharpe_ratio": 0.65,
"max_drawdown": -0.1911,
"trades": [
{ "date": "2020-10-20", "price": 2739.0, "side": "BUY" },
{ "date": "2022-05-06", "price": 3432.6, "side": "SELL" }
],
"equity_curve": [...],
"dates": [...]
}


## Future Improvements

- Add more strategies (breakout, Bollinger Bands, etc.).
- Compare multiple strategies side‑by‑side.
- Persist backtest results and allow sharing links.
- Deploy backend and frontend to the cloud.

---

This project was built as a practical trading‑strategy sandbox and portfolio piece, demonstrating full‑stack development, quantitative analytics, and UI design.


