import asyncio
from agents import Agent, Runner
import json
from pydantic import BaseModel




from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """도시의 날씨를 반환하는 함수입니다.

    Args:
        city (str): 날씨를 알고 싶은 도시명 (예: 속초, 강릉, 평창 등의 구체적인 도시명)

    Returns:
        str: 해당 도시의 날씨 정보
    """
    print(f"{city}의 날씨를 구하는 중")
    weather_dict = {
        "속초": "흐림",
        "강릉": "맑음",
        "평창": "눈"
    }
    return weather_dict.get(city, "비")



async def main():
   agent = Agent(
       name="여행 에이전트",
       instructions="당신은 훌륭한 여행 에이전트입니다.",
       model="gpt-4o-mini",
       tools=[get_weather]
   )
   prompt = """
   강원도 여행지 추천해줘 각 여행지마다 날씨도 알려줘
   """

   result = await Runner.run(agent, prompt)
   result = result.final_output
   print(result)


if __name__ == "__main__":
   asyncio.run(main())  # Run the async function