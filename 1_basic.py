import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

async def main():
   agent = Agent(
       name="여행 에이전트",
       instructions="당신은 훌륭한 여행 에이전트입니다.",
       model="gpt-4.1"
   )
   prompt = "강원도 여행지 추천해줘"
   result = await Runner.run(agent, prompt)
   print(result.final_output)    
   
if __name__ == "__main__":
   asyncio.run(main())  
