from fastapi import FastAPI,Request
from pydantic import BaseModel
import yfinance
class StockDetails(BaseModel):
    symbol: str
    name: str
    sector: str


@app.get("/stock/{symbol}")
async def get_stock(symbol: str,):
    data=yfinance.ticker(symbol)
    stockdetails = StockDetails(symbol=symbol, name=data.name, sector=data.sector)
    return stockdetails.model_dump()
