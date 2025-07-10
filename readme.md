# 🧠 OpenAI Agents SDK 뽀개기

## OpenAI Agents SDK 소개
- OpenAI가 개발한 에이전트 개발 프레임워크로, Python 기반의 멀티 에이전트 워크플로우를 쉽게 구현할 수 있습니다.
- “에이전트를 구축하기 위한 실용적인 가이드”에서 활용되며, 웹 검색, 파일 검색, 컴퓨터 제어 등 다양한 도구와 결합해 사용됩니다 [\[OpenAI Agents SDK 소개 가이드\]](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf).
- 경량 SDK이지만 handoffs, guardrails, tracing, structured output 등의 고급 기능도 포함되어 있어 개발 생산성을 대폭 높여줍니다
---

## 📌 Details

<details>
<summary>1. 기본 에이전트 구현</summary>

### 1_ 기본 에이전트  
- **[1_basic.py](./1_basic.py)**: 가장 단순한 에이전트 구조 구현 예제

</details>

<details>
<summary>2. 대화형 에이전트</summary>

### 2_1 채팅 기본  
- **[2_1_chat.py](./2_1_chat.py)**: 기본적인 채팅 기능 구현

### 2_2 스트리밍 채팅  
- **[2_2_chat_stream.py](./2_2_chat_stream.py)**: 스트리밍 응답 기능 구현

### 2_3 Chat UI  
- **[2_3_chat_ui.py](./2_3_chat_ui.py)**: 간단한 챗 인터페이스 구성

</details>

<details>
<summary>3. 도구(Tool) 사용</summary>

### 3_1 내장 툴  
- **[3_1_tool.py](./3_1_tool.py)**: Built‑in Tool 사용 예제

### 3_2 웹 검색  
- **[3_2_tool_websearch.py](./3_2_tool_websearch.py)**: 웹 검색 툴 통합

### 3_3 MCP 연동  
- **[3_3_tool_mcp.py](./3_3_tool_mcp.py)**: MCP 기반 툴 사용

### 3_4 Agent-as-Tool  
- **[3_4_tool_agentastool.py](./3_4_tool_agentastool.py)**: 에이전트를 도구처럼 활용

### 3_5 Tool‑기반 UI  
- **[3_5_tool_ui.py](./3_5_tool_ui.py)**: Tool 중심 UI 예제

</details>

<details>
<summary>4. 고급 기능</summary>

### 4_1 문맥 관리  
- **[4_1_context.py](./4_1_context.py)**: Context 관리

### 4_2 구조화된 출력  
- **[4_2_structured_output.py](./4_2_structured_output.py)**: Pydantic을 활용한 구조화된 출력

### 4_3 Guardrail  
- **[4_3_guardrail.py](./4_3_guardrail.py)**: Guardrail 적용 예시

### 4_4 핸드오프 트리아지  
- **[4_4_handoff_triage.py](./4_4_handoff_triage.py)**: Handoff 시나리오 구현

</details>

<details>
<summary>5. 최종 에이전트 완성</summary>

### 5_ 최종 통합  
- **[5_final_agent.py](./5_final_agent.py)**: 모든 기능을 통합한 완전한 에이전트 구현

</details>

<details>
<summary>6. 기타 팁</summary>

### 6_ 노트북 팁  
- **[6_tips.ipynb](./6_tips.ipynb)**: tracing, 타 LLM 연동 등 고급 팁 정리

</details>
