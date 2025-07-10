import asyncio
from pydantic import BaseModel
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

# ─────────────────────────────
# 🧰 여행 날씨 확인 함수
# ─────────────────────────────

@function_tool
def get_weather(city: str) -> str:
    """도시의 날씨를 반환하는 함수입니다."""
    print(f"{city}의 날씨를 구하는 중")
    weather_dict = {
        "속초": "흐림",
        "강릉": "맑음",
        "평창": "눈"
    }
    return weather_dict.get(city, "비")

# ─────────────────────────────
# 🔒 Guardrail 관련 구성
# ─────────────────────────────

# guardrail의 출력 타입 정의
class TravelRelevanceOutput(BaseModel):
    travel_unrelated: bool
    explanation: str

# guardrail용 agent: 입력이 여행 관련인지 판단
guardrail_agent = Agent(
    name="여행 관련 여부 판단기",
    instructions=(
        "사용자의 입력이 여행 계획이나 여행 질문과 관련된 것인지 판단하세요. "
        "여행 관련 질문(예: 장소 추천, 일정 계획, 날씨 문의 등)이면 'travel_unrelated=False', "
        "그 외(예: 수학 문제, 철학 질문 등)면 True로 출력하세요."
    ),
    output_type=TravelRelevanceOutput,
)

# input guardrail 함수 정의
@input_guardrail
async def travel_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        tripwire_triggered=result.final_output.travel_unrelated,
        output_info=result.final_output, ## return full output
    )

# ─────────────────────────────
# 🧳 여행 에이전트 정의
# ─────────────────────────────

agent = Agent(
    name="여행 에이전트",
    instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.",
    tools=[get_weather],
    input_guardrails=[travel_input_guardrail]
)

# ─────────────────────────────
# 💬 대화 루프
# ─────────────────────────────

async def chat_with_agent():
    messages = []

    while True:
        user_input = input("\n사용자: ")
        if user_input.strip().lower() == "exit":
            print("Bye")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = await Runner.run(agent, input=messages)
            messages.append({"role": "assistant", "content": response.final_output})
            print(f"\n여행 에이전트: {response.final_output}")

        except InputGuardrailTripwireTriggered:
            print("\n여행 에이전트: 여행과 관련된 질문만 도와드릴 수 있어요. 😊")

# ─────────────────────────────
# 🚀 실행 진입점
# ─────────────────────────────

if __name__ == "__main__":
    asyncio.run(chat_with_agent())
