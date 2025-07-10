import asyncio
from agents import Agent, Runner
import json
from pydantic import BaseModel

# 1 프롬프트를 활용하기
# async def main():
#    agent = Agent(
#        name="여행 에이전트",
#        instructions="당신은 훌륭한 여행 에이전트입니다.",
#        model="gpt-4o-mini"
#    )
#    prompt = """
#    강원도 여행지 추천해줘
#    각 여행지를 추천할 때 여행지 명과 평점(10점 만점)을 아래 형식으로 추천해줘
#    응답 결과만 알려줘
#    [
#       {
#          "name": "여행지 명",
#          "score": 평점
#       }
#    ]
#    """

#    result = await Runner.run(agent, prompt)
#    travel_list = json.loads(result.final_output)
#    print(travel_list)
#    for travel in travel_list:
#       print(f"{travel['name']} - {travel['score']}점")



# 2 sturctured output 사용하기
class Travel(BaseModel):
   name: str
   score: int

async def main():
   agent = Agent(
       name="여행 에이전트",
       instructions="당신은 훌륭한 여행 에이전트입니다.",
       model="gpt-4o-mini",
       output_type=list[Travel]
   )
   prompt = """
   강원도 여행지 추천해줘
   """

   result = await Runner.run(agent, prompt)
   travel_list = result.final_output
   print(travel_list)
   for travel in travel_list:
      print(f"{travel.name} - {travel.score}점")


if __name__ == "__main__":
   asyncio.run(main())  # Run the async function