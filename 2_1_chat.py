import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

async def main():
    messages = []
    agent = Agent(
        name="여행 에이전트",
        instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요."
    )
    
    while True:
        user_input = input("\n사용자: ")
        if user_input == "exit":
            print("Bye")
            break
        
        messages.append({"role": "user", "content": user_input})
        response = await Runner.run(agent, input=messages)
        messages.append({"role": "assistant", "content": response.final_output})
        
        print(f"\n여행 에이전트: {response.final_output}")
        
if __name__ == "__main__":
    asyncio.run(main())
