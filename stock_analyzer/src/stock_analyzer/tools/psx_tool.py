from crewai.tools import BaseTool
from pydantic import Field
import yfinance as yf

class PSXStockTool(BaseTool):
    name: str = "psx_stock_search"
    description: str = "Get the current price and basic financials for a stock on the Pakistan Stock Exchange using its ticker symbol."

    def _run(self, ticker: str) -> str:
        # PSX stocks in Yahoo Finance need the '.KA' suffix
        # We ensure it's there even if the agent forgets it
        if not ticker.endswith(".KA"):
            full_ticker = f"{ticker}.KA"
        else:
            full_ticker = ticker
            
        try:
            stock = yf.Ticker(full_ticker)
            info = stock.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPreviousClose')
            market_cap = info.get('marketCap', 'N/A')
            forward_pe = info.get('forwardPE', 'N/A')
            
            return f"""
            Data for {ticker}:
            - Current Price: PKR {current_price}
            - Market Cap: {market_cap}
            - Forward P/E: {forward_pe}
            - Summary: {info.get('longBusinessSummary', 'No summary available.')[:200]}...
            """
        except Exception as e:
            return f"Error fetching data for {ticker}: {str(e)}"