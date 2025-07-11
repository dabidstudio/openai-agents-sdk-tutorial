from agents import Agent, Runner
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


# ──────────────────────────────────────
# 여행일정 에이전트
# ──────────────────────────────────────
travel_agent = Agent(
    name="travel_agent",
    instructions="""
    당신은 훌륭한 여행 에이전트입니다.
    사용자에게 구체적인 여행 계획을 제시해 주세요
    친근하고 체계적인 형식으로 한국어로 응답하세요.
    """
)
# ──────────────────────────────────────
# 질문 구체화 에이전트
# ──────────────────────────────────────
clarifier_agent = Agent(
    name="clarifier_agent",
    instructions="""
    사용자의 여행 문의가 너무 모호하거나 중요한 정보가 부족한 경우, 
    2-3개의 후속 질문을 해주세요 하세요.
    문의가 이미 명확한 경우 `transfer_to_travel_agent` 호출
    예시 질문:
    - 어떤 여행지를 생각하고 계신가요?
    - 언제 여행하실 계획인가요?
    - 예산은 어느 정도인가요?
    - 자연, 모험, 문화, 휴식 중 어떤 것을 찾으시나요?

    모든 질문은 한국어로 작성하세요.
    """,
    handoffs=[travel_agent]
)

# ──────────────────────────────────────
# 분류 에이전트 (시작점)
# ──────────────────────────────────────
triage_agent = Agent(
    name="triage_agent",
    instructions="""
    사용자의 문의가 여행 계획에 사용될 준비가 되었는지 판단하세요.
    
    - 핵심 정보가 부족한 경우 `transfer_to_clarifier_agent` 호출
    - 요청이 명확하고 잘 명시된 경우 `transfer_to_travel_agent` 호출
    
    """,
    handoffs=[clarifier_agent, travel_agent]
)

async def main():

    messages = []

    while True:
        user_input = input("\n사용자: ")
        if user_input == "exit":
            print("Bye")
            break
        
        messages.append({"role": "user", "content": user_input})
        response = await Runner.run(triage_agent, input=messages)
        messages.append({"role": "assistant", "content": response.final_output})
        print(f"\n{response.last_agent.name}: {response.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
