import asyncio
from typing import List, Dict
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

async def chat_with_agent():
    messages: List[Dict[str, str]] = []

    agent = Agent(
        name="여행 에이전트",
        instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.",
        model="gpt-4.1-mini", 
    )

    print("💬 여행 에이전트와 대화를 시작합니다. 종료하려면 'exit'을 입력하세요.")

    while True:
        user_input = input("\n👤 사용자: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 대화를 종료합니다.")
            break

        # 메시지 기록에 사용자 입력 추가
        messages.append({"role": "user", "content": user_input})

        print("🤖 여행 에이전트: ", end="", flush=True)

        # 스트리밍 응답 시작
        result = Runner.run_streamed(agent, input=messages)
        full_response = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta or ""
                print(delta, end="", flush=True)
                full_response += delta

        # 메시지 기록에 에이전트 응답 추가
        messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    asyncio.run(chat_with_agent())
