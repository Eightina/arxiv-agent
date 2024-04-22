# # from agent.custom_tools.CustomStructedCrawler import crawl
# # crawl()
# import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
# from metagpt.tools.libs import CustomStructedCrawler

# async def main(requirement: str):
#     role = DataInterpreter(tools=["CustomStructedCrawler"]) # 集成工具
#     await role.run(requirement)

# if __name__ == "__main__":
#     requirement = "please crawl the latest large language models related papers from arxiv and save result"
#     asyncio.run(main(requirement))

import asyncio
import typer
from metagpt.logs import logger
from metagpt.team import Team
from agent.custom_roles.SimpleCrawler import SimpleCrawler
from agent.custom_roles.Summarizer import Summarizer

import fire

async def main(
    idea: str = "start crawl",
    investment: float = 10.0,
    n_round: int = 1,
    add_human: bool = False,
):
    logger.info(idea)

    team = Team()
    team.hire(
        [
            SimpleCrawler(),
            Summarizer(),
        ]
    )

    team.invest(investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round)


if __name__ == "__main__":
    fire.Fire(main)

# test crawler only
# from agent.custom_actions.DataActions import StructedCrawl
# s = StructedCrawl()
# res = s.run()
# print(res)