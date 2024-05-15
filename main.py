
from metagpt.logs import logger
from metagpt.team import Team
from agent.custom_roles.SimpleCrawler import SimpleCrawler
from agent.custom_roles.Summarizer import Summarizer
import fire
from tools.Messenger import MsgBody, Messenger
from tools.AccessFile import loadOrCreateRecord, saveRecord, convertPDF
from datetime import datetime
import os

async def main(
    # outputPath: str,
    idea: str = "start crawl",
    investment: float = 10.0,
    n_round: int = 1,
    add_human: bool = False,
):
    path_wk = r"/home/int.orion.que/dev/app/wkhtmltopdf/wkhtmltox/bin/wkhtmltopdf"
    today = datetime.now().date()
    outputPath = "./output/summary@{}.md".format(today)
    rawPath="./output/paper@{}.md".format(today)
   
    outputPDFPath = "./output/summary@{}.pdf".format(today)
    rawPDFPath="./output/paper@{}.pdf".format(today)
    
    
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
        
        convertPDF(outputPath, outputPDFPath, path_wk)
        convertPDF(rawPath, rawPDFPath, path_wk)
        
        msger = Messenger(key="1cb2d8e5-acd9-4d75-ae5f-2d08d0f89044")
        
        msgtoSend0 = MsgBody.TX.value
        msgtoSend0['text']['content'] = "Goodmorning! Today is {today}. New papers detected. Summary:".format(today=today)
        msger.sendMsg(msgtoSend0)
        
        mediaID0 = msger.fileup(outputPDFPath)
        filetoSend0 = MsgBody.FL.value
        filetoSend0['file']['media_id'] = mediaID0
        msger.sendMsg(filetoSend0)

        msgtoSend1 = MsgBody.TX.value
        msgtoSend0['text']['content'] = "Full list of abstrcts and links if you're interested:"
        msger.sendMsg(msgtoSend0)
        
        mediaID1 = msger.fileup(rawPDFPath) 
        filetoSend1 = MsgBody.FL.value
        filetoSend1['file']['media_id'] = mediaID1
        msger.sendMsg(filetoSend1)
        
        # clear seen papers cache every 7 days, cleaninng records 7 days ago
        if (today.day % 7 == 0):
            record = loadOrCreateRecord("./output/")
            dateToDel = []
            for date in record.keys():
                if (abs((today - date)).days >= 7):
                    dateToDel.append(date)
            for date in dateToDel:
                del record[date]
            saveRecord(record, "./output/")
                


if __name__ == "__main__":
    fire.Fire(main)
    