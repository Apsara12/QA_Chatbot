from langchain.agents import Tool, initialize_agent, AgentType
from agents.tool_agent import is_valid_email, is_valid_phone, extract_date
from llm import llm

tools = [
    Tool(name="ValidateEmail", func=is_valid_email, description="Check if an email is valid."),
    Tool(name="ValidatePhone", func=is_valid_phone, description="Check if a phone number is valid."),
    Tool(name="ExtractDate", func=extract_date, description="Extract a date from natural language."),
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
