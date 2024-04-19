import re
from metagpt.actions import Action
from metagpt.logs import logger
# class ArticleTaxonomize(Action):
#     PROMPT_TEMPLATE: str = """
#     {mdstring} \n
#     The upper markdown text contains titles, abstracts, and categories of a series
#     of new papers on large language models. Based on this widely recognized taxonomy of 
#     Large Language Models researching:
#     {internetTaxonomy} \n
#     , according to the papers'actual content, classify these papers
#     into several subjects.
#     """

#     name: str = "ArticleTaxonomize"

#     async def run(self, internetTaxonomy: str, mdstring: str) -> str:
#         prompt = self.PROMPT_TEMPLATE.format(internetTaxonomy, mdstring)

#         myTaxonomy = await self._aask(prompt)

#         return myTaxonomy

# class StructuredSummarize(Action):
#     PROMPT_TEMPLATE: str = """
#     {mdstring} \n
#     The upper markdown text contains titles, abstracts, and categories of a series
#     of new papers on large language models. Based on the strict taxonomy:
#     {myTaxonomy} \n
#     , summarize these papers by topics, metioning the titles of the referenced papers,
#     and give a summariztion of current researching trend in the end.
#     """

#     name: str = "StructuredSummarize"

#     async def run(self, mdstring: str, myTaxonomy: str) -> str:
#         prompt = self.PROMPT_TEMPLATE.format(mdstring, myTaxonomy)

#         rsp = await self._aask(prompt)

#         return rsp
    
class Summarize(Action):
    PROMPT_TEMPLATE: str = """
    {mdstring} \n
    The upper markdown text contains titles, abstracts, and categories of a series
    of new papers on large language models, summarize these papers by topics, in each
    category, give a concise summary and metion the titles of the referenced papers. 
    Finally, give a summariztion of current researching trend in the end.
    """

    name: str = "Summarize"

    async def run(self, mdstring: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(mdstring=mdstring)

        rsp = await self._aask(prompt)

        return rsp
