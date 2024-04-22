
from metagpt.logs import logger
from metagpt.roles.role import Role
from metagpt.schema import Message
# from agent.custom_actions.TextActions import ArticleTaxonomize, StructuredSummarize, Summarize
from agent.custom_actions.TextActions import Summarize, Taxonomize
from agent.custom_actions.DataActions import StructedCrawl

from metagpt.actions.research import WebBrowseAndSummarize
# from metagpt.roles.researcher import RESEARCH_PATH, Researcher

class Summarizer(Role):
    name: str = "Sam"
    profile: str = "Summarizer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_actions([ArticleTaxonomize, StructuredSummarize])
        self._watch([StructedCrawl])
        # self.set_actions([Summarize])
        self.set_actions([Taxonomize, Summarize])
        # self._watch([WebBrowseAndSummarize])
        self._set_react_mode(react_mode="by_order")
        self.outputPath = kwargs['outputPath']

    async def _act(self) -> Message:

        msg = self.get_memories()[-1]  # find the most recent messages
        # logger.debug("=====================Summarizer._act msg:===================\n"+str(len(msg)))
        if (msg.content == "") :
            logger.info("No new summary saved.")
            return ""
        
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be ArticleTaxonomize() -> StructuredSummarize()
        result = await todo.run(msg.content)
        
        # mdstring = MDoutput(inDatedEntries, outputDir + "/paper@{}.md".format(today))
        
        with open(self.outputPath, "w", encoding='UTF-8', errors='replace') as file:
            file.write(result)
        logger.info("{} saved.".format(self.outputPath))
        
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg