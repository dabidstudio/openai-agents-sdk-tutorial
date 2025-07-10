# 🧠 OpenAI Agents SDK 뽀개기

## OpenAI Agents SDK 소개
- OpenAI가 개발한 에이전트 개발 프레임워크, 파이썬으로 복잡한 에이전트 시스템 구현 가능
- OpenAI에서 발행한  [[실용적인 에이전트개발 가이드]](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)에서 활용됨
- handoffs, guardrails, tracing, structured output 등의 다양한 기능을 쉽게 구현 가능


## 설치 및 실행

1. 필수 패키지 설치  
   ```bash
   uv add openai-agents streamlit python-dotenv
   ```

2. 환경 변수 파일(.env)을 생성한 후, OpenAI API 키를 입력.
   ```env
   OPENAI_API_KEY=여기에_발급받은_키_입력
   ```

3. Streamlit 앱 실행  
   ```bash
   uv run 1_basic.py
   ```



## 주제별 코드

<details>
<summary>1. 기본 에이전트 구현</summary>

<img width="827" height="433" alt="image" src="https://github.com/user-attachments/assets/b453d1d8-ff71-47d8-80c0-64baffc584d6" />

- [1_basic.py](./1_basic.py): 첫 에이전트 만들기

</details>

<details>
<summary>2. 대화형 에이전트</summary>
<img width="755" height="491" alt="image" src="https://github.com/user-attachments/assets/8b3fba86-e060-4b6a-950a-e519f6cc78a7" />


- [2_1_chat.py](./2_1_chat.py): 대화형 에이전트 구현
- [2_2_chat_stream.py](./2_2_chat_stream.py): 스트림 기능 구현
- [2_3_chat_ui.py](./2_3_chat_ui.py): 챗 UI 구현

</details>

<details>
<summary>3. 도구(Tool) 사용</summary>

<img width="867" height="543" alt="image" src="https://github.com/user-attachments/assets/90c14d6a-d050-44e3-aae9-4603ca39f4e9" />

- [3_1_tool.py](./3_1_tool.py): 함수로 도구(tool) 만들기
- [3_2_tool_websearch.py](./3_2_tool_websearch.py): 내장된 도구 활용
- [3_3_tool_mcp.py](./3_3_tool_mcp.py): MCP 도구 활용
- [3_4_tool_agentastool.py](./3_4_tool_agentastool.py): 에이전트를 도구처럼 활용\
- [3_5_tool_ui.py](./3_5_tool_ui.py): UI에서 도구사용 반영하기

</details>

<details>
<summary>4. 고급 기능</summary>


- [4_1_context.py](./4_1_context.py): Context 관리

<img width="819" height="531" alt="image" src="https://github.com/user-attachments/assets/870c287e-33d5-4d71-924e-0c35122eb59b" />


- [4_2_structured_output.py](./4_2_structured_output.py): 구조화된 출력
- [4_3_guardrail.py](./4_3_guardrail.py): Guardrail 적용
<img width="1004" height="551" alt="image" src="https://github.com/user-attachments/assets/6e3c8669-f627-45b3-9a50-78a4a610ff9d" />

 
- [4_4_handoff_triage.py](./4_4_handoff_triage.py): Handoff 활용
<img width="943" height="488" alt="image" src="https://github.com/user-attachments/assets/d2b55758-ef0c-4e3f-91ec-3f24a2af2cde" />

</details>

<details>
<summary>5. 최종 에이전트 완성</summary>


- [5_final_agent.py](./5_final_agent.py): 최종 여행일정 수립 에이전트
<img width="1028" height="602" alt="image" src="https://github.com/user-attachments/assets/31ee0b42-376c-4fb9-8cfc-6cdace6c59da" />


</details>

<details>
<summary>6. 기타 팁</summary>

- [6_tips.ipynb](./6_tips.ipynb): tracing 및 다른 LLM 연동법

</details>
