# OpenAI Agents SDK 뽀개기

## OpenAI Agents SDK 소개
- OpenAI가 개발한 [에이전트 개발 프레임워크](https://openai.github.io/openai-agents-python), 파이썬으로 복잡한 에이전트 시스템 구현 가능
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

- [1_basic.py](./1_basic.py): 첫 에이전트 만들기

<div align="center">
  <img src="https://github.com/user-attachments/assets/b453d1d8-ff71-47d8-80c0-64baffc584d6" width="500" />
</div>

</details>

<details>
<summary>2. 대화형 에이전트</summary>

- [2_1_chat.py](./2_1_chat.py): 대화형 에이전트 구현  
- [2_2_chat_stream.py](./2_2_chat_stream.py): 스트림 기능 구현  
- [2_3_chat_ui.py](./2_3_chat_ui.py): 챗 UI 구현

<div align="center">
  <img src="https://github.com/user-attachments/assets/8b3fba86-e060-4b6a-950a-e519f6cc78a7" width="500" />
</div>

</details>

<details>
<summary>3. 도구(Tool) 사용</summary>

- [3_1_tool.py](./3_1_tool.py): 함수 및 내장된 도구(tool) 활용
- [3_2_tool_mcp.py](./3_2_tool_mcp.py): MCP 도구 활용  
- [3_3_tool_agents.py](./3_3_tool_agents.py): 에이전트를 도구처럼 활용  

<div align="center">
  <img src="https://github.com/user-attachments/assets/90c14d6a-d050-44e3-aae9-4603ca39f4e9" width="500" />
</div>

</details>

<details>
<summary>4. 고급 기능</summary>

- [4_1_context.py](./4_1_context.py): Context 관리  
  <details>
    <summary>이미지 보기</summary>
    <div align="center">
      <img src="https://github.com/user-attachments/assets/870c287e-33d5-4d71-924e-0c35122eb59b" width="500" />
    </div>
  </details>

- [4_2_structured_output.py](./4_2_structured_output.py): 구조화된 출력

- [4_3_guardrail.py](./4_3_guardrail.py): Guardrail 적용  
  <details>
    <summary>이미지 보기</summary>
    <div align="center">
      <img src="https://github.com/user-attachments/assets/6e3c8669-f627-45b3-9a50-78a4a610ff9d" width="500" />
    </div>
  </details>

- [4_4_handoff.py](./4_4_handoff.py): Handoff 활용  
  <details>
    <summary>이미지 보기</summary>
    <div align="center">
      <img src="https://github.com/user-attachments/assets/dfb2d8b9-7bbf-4735-b8d2-219c43956ac5" width="500" />
    </div>
  </details>

</details>

<details>
<summary>5. 최종 에이전트 완성</summary>

- [5_final_agent.py](./5_final_agent.py): 최종 여행일정 수립 에이전트

<div align="center">
  <img src="https://github.com/user-attachments/assets/0d758945-9f05-4a75-9ac3-7cdf66c71a8b" width="500" />
</div>


</details>

<details>
<summary>6. 기타 팁</summary>

- [6_1_gemini.py](./6_1_gemini.py): gemini llm 연동
- [6_2_tracing.py](./6_2_tracing.py): tracing 소개
</details>
