from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
from pydantic import SecretStr
from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)


def get_response_from_ai_agent(model: str, query, allow_search, system_prompt: str):

    logger.info(f"loading the llm from key {settings.GROQ_API_KEY}")
    llm = ChatGroq(model=model, api_key=SecretStr(
        settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None)

    logger.info(f"loading the llms {llm}")

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    logger.info("loaded the agent")
    response = agent.invoke({"messages": query})
    messages = response.get("messages", [])

    ai_messages = [
        message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1]
