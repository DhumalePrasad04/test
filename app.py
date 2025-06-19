from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Pydantic model for stock details
class StockDetails(BaseModel):
    symbol: str
    name: str | None = None
    sector: str | None = None
    current_price: float | None = None

@app.get("/stock/{symbol}", response_model=StockDetails)
async def get_stock(symbol: str):
    """
    Retrieve stock details (name, sector, current price) for a given symbol.
    """
    # Normalize symbol to uppercase
    symbol = symbol.upper()

    try:
        # Fetch stock data using yfinance
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Validate response
        if not info or "symbol" not in info:
            logger.warning(f"No data found for symbol: {symbol}")
            raise HTTPException(status_code=404, detail=f"Stock symbol '{symbol}' not found")

        # Extract stock details safely
        stock_details = StockDetails(
            symbol=symbol,
            name=info.get("longName", "N/A"),
            sector=info.get("sector", "N/A"),
            current_price=info.get("currentPrice", info.get("regularMarketPrice"))
        )

        # Ensure current_price is available
        if stock_details.current_price is None:
            logger.warning(f"Current price unavailable for symbol: {symbol}")
            raise HTTPException(status_code=404, detail=f"Current price not available for '{symbol}'")

        logger.info(f"Successfully fetched data for symbol: {symbol}")
        return stock_details

    except KeyError as e:
        logger.error(f"Missing key in yfinance response for {symbol}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Invalid or incomplete data for '{symbol}'")
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch stock data: {str(e)}")