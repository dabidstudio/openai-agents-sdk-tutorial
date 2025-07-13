import asyncio
from agents import (
    Agent,
    Runner,
    function_tool,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
)
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

# guardrail의 출력 타입 정의
class TravelRelevanceOutput(BaseModel):
    is_travel: bool
    explanation: str

# guardrail용 agent: 입력이 여행 관련인지 판단
guardrail_agent = Agent(
    name="가드레일 에이전트",
    instructions=(
        "사용자의 입력이 여행 계획이나 여행 질문과 관련된 것인지 판단하세요. "
        "그래서 여행 관련 질문(예: 장소 추천, 일정 계획, 날씨 문의 등)이면  'is_travel=True', "
        "그 외 여행과 관련이 없으면 'is_travel=False'로 출력하세요."
    ),
    output_type=TravelRelevanceOutput,
)

@input_guardrail
async def travel_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_travel,
    )



async def main():
    messages = []
    agent = Agent(
        name="여행 에이전트",
        instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.",
        input_guardrails=[travel_input_guardrail]
    )
    
    while True:
        user_input = input("\n사용자: ")
        if user_input == "exit":
            print("Bye")
            break
        
        messages.append({"role": "user", "content": user_input})
       
        try:
            response = await Runner.run(agent, input=messages)
            messages.append({"role": "assistant", "content": response.final_output})   
            print(f"\n여행 에이전트: {response.final_output}")
        except InputGuardrailTripwireTriggered:
            print("\n여행 에이전트: 여행과 관련된 질문만 도와드릴 수 있어요. 😊")
        
if __name__ == "__main__":
    asyncio.run(main())
