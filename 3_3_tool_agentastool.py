import asyncio
from agents import Agent, Runner, function_tool
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

# 날씨 정보를 반환하는 Weather Agent
weather_agent = Agent(
    name="날씨 에이전트",
    instructions=(
        "당신은 특정 도시의 날씨를 알려주는 에이전트입니다. "
        "입력으로 도시명을 받으면 해당 도시의 날씨를 알려주세요. "
        "날씨 도구를 이용해서 날씨를 알려주세요."
    ),
    model="gpt-4o-mini",
    tools=[get_weather]
)

# 여행 추천 및 날씨를 종합하는 오케스트레이터 에이전트
travel_agent = Agent(
    name="여행 에이전트",
    instructions=(
        "당신은 훌륭한 여행 에이전트입니다. "
        "강원도 내 여행지를 추천하고, 각 여행지에 대해 날씨를 알고 싶다면 "
        "제공된 날씨 에이전트 툴을 사용하세요."
    ),
    model="gpt-4o-mini",
    tools=[
        weather_agent.as_tool(
            tool_name="get_weather",
            tool_description="도시 이름을 입력하면 해당 도시의 날씨를 알려줍니다."
        )
    ],
)

async def main():
    prompt = """
    강원도 여행지 추천해줘. 각 여행지마다 날씨도 알려줘.
    """
    result = await Runner.run(travel_agent, input=prompt)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
