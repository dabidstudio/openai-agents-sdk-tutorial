import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
load_dotenv()
from openai import AsyncOpenAI
#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# client = AsyncOpenAI(
#     api_key="ollama",  # Ollama는 키 검증 안 함, 아무 값이나 가능
#     base_url="http://localhost:11434/v1",  # Ollama 서버 엔드포인트
# )


async def main():
   agent = Agent(
       name="여행 에이전트",
       instructions="당신은 훌륭한 여행 에이전트입니다.",
       model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),

   )
   prompt = "강원도 여행지 추천해줘"
   result = await Runner.run(agent, prompt)
   print(result.final_output)

if __name__ == "__main__":
   asyncio.run(main())  
