from agents import Agent, Runner, trace
from dotenv import load_dotenv
load_dotenv()
# 두 개의 에이전트 생성
joke_agent = Agent(
    name="유머 에이전트",
    instructions="당신은 유머러스한 한국어 에이전트입니다. 주어진 주제에 대해 재미있는 농담을 만들어주세요.",
)

translator_agent = Agent(
    name="번역 에이전트",
    instructions="당신은 전문 번역가입니다. 주어진 텍스트를 영어로 번역해주세요.",
)


async def main():
    with trace("유머 번역 워크플로우"):
        joke_result = await Runner.run(joke_agent, "컴퓨터")
        print("한국어 농담:", joke_result.final_output)

        # 2단계: 농담 번역
        translation_result = await Runner.run(
            translator_agent, 
            f"다음 농담을 영어로 번역해주세요: {joke_result.final_output}"
        )
        print("\n영어 번역:", translation_result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
