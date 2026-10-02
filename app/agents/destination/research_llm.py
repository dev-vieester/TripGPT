from langchain_openrouter import ChatOpenRouter

# from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

# research_llm = ChatGoogleGenerativeAI(
#     model=settings.google_model,
#     temperature=0,
#     api_key=settings.google_api_key,
#     timeout=20,
#     max_retries=2,
# )

research_llm = ChatOpenRouter(
    model="inclusionai/ling-3.0-flash-vl",
    temperature=0,
    api_key=settings.openrouter_api_key
)
