from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import yfinance as yf
class StockDetails(BaseModel):
    symbol: str | None = None
    name: str | None=None
    sector: str |None = None
    current_price: float |None =None


app = FastAPI()


@app.get("/stock/{symbol}")
async def get_stock(symbol: str,):
    symbol = symbol.upper()
    try :
        ticker=yf.Ticker(symbol)
        info = ticker.info
        if info is None:
            raise HTTPException(status_code=404,detail="Stock not found ")
        stockdetail=StockDetails(
            symbol=symbol,
            name=info["name"],
            sector=info["sector"],
            current_price=info["current_price"],
        )
        return stockdetail.model_dump()
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
