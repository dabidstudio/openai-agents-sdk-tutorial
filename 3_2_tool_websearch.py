import asyncio
from agents import Agent, Runner
from agents import Agent, function_tool, WebSearchTool

@function_tool
def get_weather(city: str) -> str:
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
       instructions="당신은 훌륭한 여행 에이전트입니다. 각 여행지에 대한 정보는 인터넷 검색 기능을 이용해줘",
       model="gpt-4o-mini",
       tools=[get_weather, WebSearchTool()]
   )
   prompt = """
   강원도 여행지 3곳을 추천해줘 각 여행지마다 날씨도 알려줘
   """

   result = await Runner.run(agent, prompt)
   result = result.final_output
   print(result)


if __name__ == "__main__":
   asyncio.run(main())  # Run the async function