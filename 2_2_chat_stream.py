import asyncio
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent


async def main():
    messages = []

    agent = Agent(
        name="여행 에이전트",
        instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.",
    )
    while True:
        user_input = input("\n사용자: ")
        if user_input == "exit":
            print("Bye")
            break\
        
        messages.append({"role": "user", "content": user_input})
        print("\n여행 에이전트: ", end="", flush=True)                

        result = Runner.run_streamed(agent, input=messages)
        full_response = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta or ""
                print(delta, end="", flush=True)
                full_response += delta                

        messages.append({"role": "assistant", "content": full_response})
                
                
                
if __name__ == "__main__":
    asyncio.run(main())