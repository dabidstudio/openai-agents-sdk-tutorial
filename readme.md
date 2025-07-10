# 🧠 OpenAI Agents SDK 뽀개기


### OpenAI Agents SDK 소개
- OpenAI가 개발한 에이전트개발 프레임워크 
- OpenAI의 "에이전트 개발을 위한 실용적인 가이드"에서 활용 https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

<details>
<summary>1️⃣ 기본 에이전트 구현</summary>

- [1_basic.py](./1_basic.py)  
  가장 단순한 에이전트 구조를 구현합니다.

</details>

---

<details>
<summary>2️⃣ 대화형 에이전트</summary>

- [2_1_chat.py](./2_1_chat.py)  
  기본적인 채팅 기능 구현

- [2_2_chat_stream.py](./2_2_chat_stream.py)  
  스트리밍 응답을 구현하는 예제

- [2_3_chat_ui.py](./2_3_chat_ui.py)  
  간단한 Chat UI 인터페이스 구현

</details>

---

<details>
<summary>3️⃣ 도구(Tool) 사용</summary>

- [3_1_tool.py](./3_1_tool.py)  
  Built-in Tool을 사용하는 예제

- [3_2_tool_websearch.py](./3_2_tool_websearch.py)  
  웹 검색 툴 통합

- [3_3_tool_mcp.py](./3_3_tool_mcp.py)  
  MCP를 툴로 활용

- [3_4_tool_agentastool.py](./3_4_tool_agentastool.py)  
  Agent를 Tool처럼 활용하는 구조

- [3_5_tool_ui.py](./3_5_tool_ui.py)  
  Tool 기반 UI 구성 예제

</details>

---

<details>
<summary>4️⃣ 고급 기능</summary>

- [4_1_context.py](./4_1_context.py)  
  문맥(Context) 관리

- [4_2_structured_output.py](./4_2_structured_output.py)  
  구조화된 출력 (Structured Output)

- [4_3_guardrail.py](./4_3_guardrail.py)  
  Guardrail 적용 예시

- [4_4_handoff_triage.py](./4_4_handoff_triage.py)  
  핸드오프(Handoff) 시나리오

</details>

---

<details>
<summary>5️⃣ 최종 에이전트 완성</summary>

- [5_final_agent.py](./5_final_agent.py)  
  모든 기능을 통합한 최종 에이전트 구현

</details>

---

<details>
<summary>6️⃣ 기타 팁</summary>

- [6_tips.ipynb](./6_tips.ipynb)  
  Tracing, 타 LLM 연동 등 고급 팁 정리

</details>
```
