import os
from langchain.chat_models import init_chat_model
import dotenv

dotenv.load_dotenv()

llm = init_chat_model(
    model="openai/gpt-oss-20b:free",   # or any OpenRouter-supported model
    model_provider="openai",
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

response = llm.invoke("Explain transformers in simple terms")
print(response.content)
