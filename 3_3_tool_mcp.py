import asyncio
from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio
import shutil


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
    # Playwright MCP 서버 실행
    async with MCPServerStdio(
        name="Playwright MCP",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"]
        }
    ) as mcp_server:


        agent = Agent(
            name="여행 에이전트",
            instructions="당신은 훌륭한 여행 에이전트입니다. 각 여행지에 대한 정보는 인터넷 검색이나 MCP 브라우저 도구를 이용해줘.",
            model="gpt-4o-mini",
            tools=[get_weather],
            mcp_servers=[mcp_server]
        )

        prompt = """
        강원도 여행지 3곳을 추천해줘 네이버 블로그를 참고해줘
        """

        result = await Runner.run(agent, prompt)
        print(result.final_output)



if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    asyncio.run(main())
