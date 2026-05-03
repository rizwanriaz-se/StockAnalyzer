from .crew import StockAnalyzerCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'stock_symbol': 'SYS', # You can change this to any ticker
        'current_year': '2026'
    }
    StockAnalyzerCrew().crew().kickoff(inputs=inputs)