from crewai.tools import tool
import json
import os

@tool("read_portfolio_ledger")
def read_portfolio_ledger(query: str="") -> dict:
    """
    Reads the ledger.json file and returns structured portfolio data.
    """
    try:
        file_path = os.path.join(os.getcwd(), "ledger.json")
        
        with open(file_path, "r") as f:
            data = json.load(f)  # ✅ parsed JSON

        return data  # ✅ structured output

    except Exception as e:
        return {"error": str(e)}