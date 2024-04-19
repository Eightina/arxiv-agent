
from metagpt.logs import logger
from metagpt.roles.role import Role
from metagpt.schema import Message
# from agent.custom_actions.TextActions import ArticleTaxonomize, StructuredSummarize, Summarize
from agent.custom_actions.TextActions import Summarize
from agent.custom_actions.DataActions import StructedCrawl
from metagpt.actions import UserRequirement
from metagpt.actions.research import WebBrowseAndSummarize
# from metagpt.roles.researcher import RESEARCH_PATH, Researcher

class SimpleCrawler(Role):
    name: str = "Sim"
    profile: str = "SimpleCrawler"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_actions([ArticleTaxonomize, StructuredSummarize])
        self._watch([UserRequirement])
        self.set_actions([StructedCrawl])
        # self._watch([WebBrowseAndSummarize])

    # async def _act(self) -> Message:
    #     logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
    #     todo = self.rc.todo  # todo will be ArticleTaxonomize() -> StructuredSummarize()

    #     msg = self.get_memories()  # find the most recent messages
    #     result = await todo.run(msg.content)
    #     msg = Message(content=result, role=self.profile, cause_by=type(todo))
    #     self.rc.memory.add(msg)
    #     return msg