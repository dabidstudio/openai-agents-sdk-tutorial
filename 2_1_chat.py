import asyncio
from agents import Agent, Runner
from typing import List, Dict

async def chat_with_agent():
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
        # 사용자 입력을 메시지 기록에 추가
        messages.append({"role": "user", "content": user_input})
        # 에이전트에게 메시지 기록을 전달하여 응답 받기
        response = await Runner.run(agent, input=messages)
        # 에이전트의 응답을 메시지 기록에 추가
        messages.append({"role": "assistant", "content": response.final_output})
        
        print(f"\n여행 에이전트: {response.final_output}")

if __name__ == "__main__":
    asyncio.run(chat_with_agent())
