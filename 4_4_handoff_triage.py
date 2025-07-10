from agents import Agent, Runner, handoff
from pydantic import BaseModel
from typing import List
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX



# ──────────────────────────────────────
# 여행 플래너 (최종 에이전트)
# ──────────────────────────────────────
travel_planner_agent = Agent(
    name="Travel Planner",
    instructions="""
    당신은 도움이 되는 여행 플래너입니다. 사용자의 명확한 여행 요구사항이 주어지면,
    목적지 제안, 활동, 샘플 일정을 포함한 여행 계획을 생성하세요.
    친근하고 체계적인 형식으로 한국어로 응답하세요.
    """
)


# ──────────────────────────────────────
# 명확화 에이전트
# ──────────────────────────────────────
clarifier_agent = Agent(
    name="Clarifier Agent",
    instructions="""
    사용자의 여행 문의가 너무 모호하거나 중요한 정보가 부족한 경우, 2-3개의 후속 질문을 통해 명확히 하세요.
    문의가 이미 명확한 경우 `transfer_to_instruction_builder`를 직접 호출하세요.
    예시 질문:
    - 어떤 여행지를 생각하고 계신가요?
    - 언제 여행하실 계획인가요?
    - 예산은 어느 정도인가요?
    - 자연, 모험, 문화, 휴식 중 어떤 것을 찾으시나요?

    모든 질문은 한국어로 작성하세요.
    """,
    handoffs=[travel_planner_agent]
)

# ──────────────────────────────────────
# 분류 에이전트 (시작점)
# ──────────────────────────────────────
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    사용자의 문의가 여행 계획에 사용될 준비가 되었는지 판단하세요.
    
    - 핵심 정보가 부족한 경우 `transfer_to_clarifier_agent` 호출
    - 요청이 명확하고 잘 명시된 경우 `transfer_to_instruction_builder` 호출
    
    하나의 함수 호출만 반환하세요.
    모든 응답은 한국어로 작성하세요.
    """,
    handoffs=[clarifier_agent, travel_planner_agent]
)

# ──────────────────────────────────────
# Runner
# ──────────────────────────────────────
async def travel_chat():
    print("\n🧳 여행 계획을 도와드릴게요! 질문해주세요 (exit 입력 시 종료)\n")

    user_input = input("사용자: ")
    if user_input.strip().lower() == "exit":
        print("안녕히 가세요!")
        return

    messages = [{"role": "user", "content": user_input}]
    clarification_rounds = 0
    MAX_ROUNDS = 5

    while True:
        response = await Runner.run(triage_agent, input=messages)
        # 1. 명확한 정보를 위한 추가 질문이 필요한 경우
        print("현재 에이전트: ", response.last_agent.name)
        if response.last_agent.name == "Clarifier Agent":
            clarification_rounds += 1
            if clarification_rounds > MAX_ROUNDS:
                print("\n⚠️ 너무 많은 질문 반복으로 중단합니다.")
                break
            print(response.final_output)
            user_reply = input("\n추가 답변: ")
            messages.append({"role": "user", "content": user_reply})
            continue

        # 2. 여행 에이전트로 요청이 전달된 경우 → 최종 응답 출력
        print(f"\n여행 에이전트: {response.final_output}")
        messages.append({"role": "assistant", "content": str(response.final_output)})
        break

if __name__ == "__main__":
    asyncio.run(travel_chat())
