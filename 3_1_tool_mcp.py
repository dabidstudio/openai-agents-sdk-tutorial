import asyncio
from agents import Agent, Runner, function_tool, WebSearchTool
from agents.mcp import MCPServerStdio


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


    async with MCPServerStdio(
        name="Playwright MCP",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"]
        }
    ) as mcp_server:

        agent = Agent(
            name="여행 에이전트",
            model="gpt-4.1-mini",
            instructions="당신은 훌륭한 여행 에이전트입니다. 여행일정을 짤 때 웹검색도 꼭 해주고 출처도 같이 표시해줘",
            mcp_servers=[mcp_server]
            
        )
        prompt = "평창 여행일정을 짜주고 날씨도 고려해줘"
        result = await Runner.run(agent, prompt)
        print(result.final_output)
   
   
if __name__ == "__main__":
   asyncio.run(main())  