from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool
from .tools.psx_tool import PSXStockTool
from stock_analyzer.tools.ledger_reader import read_portfolio_ledger

# We'll use a placeholder for your custom PSX tool for now
# from stock_analyzer.tools.psx_tool import PSXStockTool

# Use the big brain for the final strategy
smart_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    )

# Use the fast, high-limit model for data gathering
fast_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    )

@CrewBase
class StockAnalyzerCrew():
    """StockAnalyzer crew for Macro and Portfolio analysis"""

    # These point to your YAML files automatically
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def portfolio_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['portfolio_auditor'],
            # tools=[FileReadTool(file_path='ledger.json')], # To read your ledger.json/csv
            tools=[read_portfolio_ledger], # Using our custom tool to read the ledger
            verbose=True,
            llm=fast_llm,  # Pass it here!,
            allow_delegation=False,
            
        )

    @agent
    def macro_economist(self) -> Agent:
        return Agent(
            config=self.agents_config['macro_economist'],
            tools=[SerperDevTool()], # To check fuel, war, and global news
            verbose=True
        )

    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'],
            tools=[PSXStockTool()], # We will build this next
            verbose=True
        )

    @agent
    def investment_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_strategist'],
            verbose=True,
            llm=smart_llm,  # Pass the big brain here!
        )

    @task
    def audit_ledger_task(self) -> Task:
        return Task(
            config=self.tasks_config['audit_ledger_task']
        )

    @task
    def macro_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['macro_analysis_task']
        )

    @task
    def market_valuation_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_valuation_task']
        )

    @task
    def strategic_advice_task(self) -> Task:
        return Task(
            config=self.tasks_config['strategic_advice_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalyzer crew"""
        return Crew(
            agents=self.agents, # Automatically collects methods marked with @agent
            tasks=self.tasks,   # Automatically collects methods marked with @task
            process=Process.sequential, # One by one: Audit -> Macro -> Market -> Strategy
            verbose=True,
            max_rpm=1
        )