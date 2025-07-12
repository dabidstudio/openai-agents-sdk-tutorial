## 1회 실행 시 약 입력토큰 50만 / 출력토큰 0.1만, gpt-4.1 약 1불

import re
import sys
import asyncio
import streamlit as st
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from openai.types.responses import (
    ResponseTextDeltaEvent,
    ResponseOutputItemDoneEvent,
    ResponseFunctionToolCall
)
from agents import (
    Agent, Runner, function_tool,
    input_guardrail,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered,
    RunContextWrapper, TResponseInputItem
)
from agents.mcp import MCPServerStdio
from datetime import datetime, timezone, timedelta

load_dotenv()






# ─────────────────────────────
# 스트림릿 관련
# ─────────────────────────────

# Windows 스트림릿 호환성 설정
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def sanitize_markdown(text):
    # 숫자 범위에 사용된 물결표를 이스케이프 처리 (예: 6~10 -> 6\~10)
    return re.sub(r'(\d)~(\d)', r'\1\~\2', text)

# ─────────────────────────────
# 도구 관련
# ─────────────────────────────
@function_tool()
def get_weather(city: str) -> str:
    """도시의 날씨를 반환하는 함수입니다.

    Args:
    city (str): 날씨를 알고 싶은 도시명 (예: 속초, 강릉, 평창 등의 구체적인 도시명)

    Returns:
    str: 해당 도시의 날씨 정보
    """
    print(f"{city}의 날씨를 구하는 중")
    weather_dict = {
        "속초": "흐림, 18°C",
        "강릉": "맑음, 20°C", 
        "평창": "눈, -2°C",
        "춘천": "맑음, 19°C",
        "원주": "흐림, 17°C",
        "동해": "맑음, 19°C",
        "태백": "흐림, 12°C",
        "삼척": "맑음, 18°C",
        "홍천": "맑음, 16°C",
        "횡성": "흐림, 15°C",
        "영월": "맑음, 17°C",
        "정선": "흐림, 14°C",
        "철원": "맑음, 16°C",
        "화천": "흐림, 15°C",
        "양구": "맑음, 16°C",
        "인제": "흐림, 14°C",
        "고성": "맑음, 17°C",
        "양양": "흐림, 18°C"
    }
    return weather_dict.get(city, "비, 15°C")



# ─────────────────────────────
# 가드레일 관련
# ─────────────────────────────
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

# ─────────────────────────────
# MCP 서버 및 에이전트 생성
# ─────────────────────────────
def create_agents(mcp_server):
    """에이전트들을 생성하는 함수"""

    # KST 타임존 생성
    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst)
    # 한국어 날짜 및 시간 포맷
    today_kst = now_kst.strftime("%Y년 %m월 %d일 %H시 %M분 KST")

    print(today_kst)
    travel_agent = Agent(
        name="tavel_agent",
        instructions=f"""
        현재 시각은 {today_kst} 입니다.
        명확한 여행 정보가 주어지면 여행 목적지, 활동, 예산 등을 포함한 상세한 계획을 한국어로 작성하세요.
        MCP 브라우저 도구나 날씨 도구를 활용할 수 있습니다.
        날씨나 인터넷을 적극적으로 활용해서 여행 계획을 작성해주세요.
        여행계획을 세울 떄는 반드시 브라우저 도구를 이용해서 각 도시에 대한 정보를 찾아줘.
        그리고 각 도시에 대한 날씨정보도 get_weather 도구를 활용해서 찾아줘.
        각 도시에서 어떤 활동을 하면 좋을지에 대한 정보는
        네이버블로그 (blog.naver.com)에 접속한 다음 각 도시 + 여행이라고 브라우저에서 검색해서 네이버 블로그 글을 클릭해서 정보를 활용해줘.
        블로그를 참고했으면 참고한 블로그 링크까지 출처로 포함해서 응답해저ㅜ
        
        """,
        model="gpt-4.1",
        tools=[get_weather],
        mcp_servers=[mcp_server]
    )

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

    triage_agent = Agent(
        name="triage_agent",
        instructions="""
        사용자의 문의가 여행 계획에 사용될 준비가 되었는지 판단하세요.
        
        - 핵심 정보가 부족한 경우 `transfer_to_clarifier_agent` 호출
        - 요청이 명확하고 잘 명시된 경우 `transfer_to_travel_agent` 호출
        
        """,
        handoffs=[clarifier_agent, travel_agent],
        input_guardrails=[travel_input_guardrail]
    )

    return triage_agent


# ─────────────────────────────
# 스트림릿 메시지 처리 함수
# ─────────────────────────────
async def process_user_message_with_mcp():
    """MCP 서버와 함께 사용자 메시지를 처리하는 함수"""
    # MCP 서버를 async context manager로 사용
    async with MCPServerStdio(
        name="Playwright MCP",
        params={"command": "npx", "args": ["@playwright/mcp@latest"]},
        cache_tools_list=True,
        client_session_timeout_seconds=30  # 타임아웃을 30초로 증가
    ) as mcp_server:
        
        # 에이전트 생성
        triage_agent = create_agents(mcp_server)
        
        # 메시지 처리
        result = Runner.run_streamed(triage_agent, input=st.session_state.messages, max_turns=20)
        response_text = ""
        placeholder = st.empty()

        async for event in result.stream_events():
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent):
                    response_text += event.data.delta or ""
                    with placeholder.container():
                        with st.chat_message("assistant"):
                            st.write(sanitize_markdown(response_text))

                if (
                    isinstance(event.data, ResponseOutputItemDoneEvent)
                    and isinstance(event.data.item, ResponseFunctionToolCall)
                ):
                    tool_name = getattr(event.data.item, "name", "알 수 없음")
                    raw_args = getattr(event.data.item, "arguments", "{}")
                    try:
                        args = json.loads(raw_args)
                        arg_str = ", ".join(f"{k}: {v}" for k, v in args.items())
                    except Exception:
                        arg_str = raw_args
                    st.toast(f"🛠 도구 활용: `{tool_name}`\nArgs: {arg_str}", icon="🛠")

        return response_text


def main():
    st.set_page_config(page_title="✈️ AI 여행 에이전트", page_icon="🌍")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("✈️ AI 여행 에이전트")
    st.caption("당신의 여행 계획을 도와드릴게요!")


    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_input = st.chat_input("어디로 여행 가고 싶으신가요?")
    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            # 메시지 처리
            response_text = asyncio.run(process_user_message_with_mcp())
            if response_text:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })
        except InputGuardrailTripwireTriggered:
            st.error("❗ 여행과 관련된 질문만 답변할 수 있습니다.")
        except Exception as e:
            st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
