import asyncio
from agents import Agent, Runner,RunContextWrapper
from agents import Agent, function_tool
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class UserContext(BaseModel):
    user_id: str
    name: str
    subscription_tier: str = "free"  # free, premium, enterprise
    
@function_tool
async def fetch_user_name(wrapper: RunContextWrapper) -> str:
    '''Returns the name of the user.'''
    return f"사용자의 이름은 {wrapper.context.name} 입니다."

def premium_feature_enabled(context: RunContextWrapper, agent: Agent) -> bool:
    return context.context.subscription_tier in ["premium", "enterprise"]

@function_tool(is_enabled=premium_feature_enabled)
def get_weather(city: str) -> str:
    """도시의 날씨를 반환하는 함수입니다.

    Args:
    city (str): 날씨를 알고 싶은 도시명 (예: 속초, 강릉, 평창 등의 구체적인 도시명)

    Returns:
    str: 해당 도시의 날씨 정보
    """
    print(f"{city}의 날씨를 구하는 중")
    weather_dict = {
        "속초": "흐림, 18°C",
        "강릉": "맑음, 20°C", 
        "평창": "눈, -2°C",
        "춘천": "맑음, 19°C",
        "원주": "흐림, 17°C",
        "동해": "맑음, 19°C",
        "태백": "흐림, 12°C",
        "삼척": "맑음, 18°C",
        "홍천": "맑음, 16°C",
        "횡성": "흐림, 15°C",
        "영월": "맑음, 17°C",
        "정선": "흐림, 14°C",
        "철원": "맑음, 16°C",
        "화천": "흐림, 15°C",
        "양구": "맑음, 16°C",
        "인제": "흐림, 14°C",
        "고성": "맑음, 17°C",
        "양양": "흐림, 18°C"
    }
    return weather_dict.get(city, "비, 15°C")

def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"사용자의 이름은 {context.context.name}.당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.답변을 할 때 사용자의 이름을 구하고 이름을 불러서 활용해주세요"


async def main():
    context = UserContext(user_id="123", name="dabid", subscription_tier="free")

    messages = []
    agent = Agent(
        name="여행 에이전트",
        instructions=dynamic_instructions,
        # instructions="당신은 훌륭한 여행 에이전트입니다. 사용자와 대화하면서 여행 계획을 도와주세요.답변을 할 때 사용자의 이름을 구하고 이름을 불러서 활용해주세요",
        tools=[get_weather,fetch_user_name],
    )
    while True:
        user_input = input("\n사용자: ")
        if user_input == "exit":
            print("Bye")
            break


        messages.append({"role": "user", "content": user_input})
        response = await Runner.run(agent, input=messages,context=context)
        messages.append({"role": "assistant", "content": response.final_output})
        
        print(f"\n여행 에이전트: {response.final_output}")
        

if __name__ == "__main__":
    asyncio.run(main())
