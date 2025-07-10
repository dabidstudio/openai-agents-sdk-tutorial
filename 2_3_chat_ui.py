import asyncio
import streamlit as st
from typing import List, Dict
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent


def init_agent() -> Agent:
    return Agent(
        name="여행 에이전트",
        instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.",
        model="gpt-4.1-mini",  # text 모델이어야 ResponseTextDeltaEvent 지원됨
    )


async def stream_response(agent: Agent, messages: List[Dict[str, str]]) -> str:
    response_text = ""
    placeholder = st.empty()

    result = Runner.run_streamed(agent, input=messages)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            delta = event.data.delta or ""
            response_text += delta
            with placeholder.container():
                with st.chat_message("assistant"):
                    st.markdown(response_text)

    return response_text


def main():
    st.set_page_config(page_title="스트리밍 여행 챗봇", page_icon="🗺️")
    st.title("🗺️ 여행 에이전트")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 대화 렌더링
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력 처리
    user_input = st.chat_input("여행 관련 질문을 입력하세요")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        agent = init_agent()
        assistant_response = asyncio.run(stream_response(agent, st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    main()
