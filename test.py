# # from agent.custom_tools.CustomStructedCrawler import crawl
# # crawl()
# import asyncio
# from metagpt.roles.di.data_interpreter import DataInterpreter
# from metagpt.tools.libs import CustomStructedCrawler

# async def main(requirement: str):
#     role = DataInterpreter(tools=["CustomStructedCrawler"])

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
from task.Messenger import MsgBody, Messenger
from datetime import datetime
import os

async def main(
    # outputPath: str,
    idea: str = "start crawl",
    investment: float = 10.0,
    n_round: int = 1,
    add_human: bool = False,
):
    today = datetime.now().date()
    outputPath = "./output/summary@{}.md".format(today)
    rawPath="./output/paper@{}.md".format(today)
    
    logger.info(idea)

    team = Team()
    team.hire(
        [
            SimpleCrawler(),
            Summarizer(outputPath=outputPath),
        ]
    )

    team.invest(investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round)
    
    if os.path.exists(outputPath):
            
        msger = Messenger(key="1cb2d8e5-acd9-4d75-ae5f-2d08d0f89044")
        
        
        # mediaID0 = msger.fileup(outputPath)
        # filetoSend0 = MsgBody.FL.value
        # filetoSend0['file']['media_id'] = mediaID0
        # msger.sendMsg(filetoSend0)
        
        mediaID1 = msger.fileup(rawPath) 
        filetoSend1 = MsgBody.FL.value
        filetoSend1['file']['media_id'] = mediaID1
        msger.sendMsg(filetoSend1)
        
        # md = MsgBody.MD.value
        # with open("output/summary-v1.1ms.md", "r") as f:
        #     mdtx = f.read()
        #     md['markdown']['content'] = mdtx
        # msger.sendMsg(md)
        
        msgtoSend0 = MsgBody.TX.value
        msgtoSend0['text']['content'] = "Bot communication testing. Sorry for the interruption."
        msger.sendMsg(msgtoSend0)

if __name__ == "__main__":
    
    fire.Fire(main)
    

        
# test crawler only
# from agent.custom_actions.DataActions import StructedCrawl
# s = StructedCrawl()
# res = s.run()
# print(res)