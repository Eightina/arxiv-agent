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
    {}
    上述文本包含了一系列最新的大语言模型领域的论文的标题，摘要，分类等内容。
    使用中文，分析每篇文章其解决的问题和方法论。
    """
    # 最后，对这些文章按一定的主题进行汇总，并总结当前大语言模型领域研究的最新趋势，突出重点。

    name: str = "Summarize"

    async def run(self, mdstring: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(mdstring)
        logger.info("======================================"+str(len(mdstring)))
        rsp = await self._aask(prompt)

        return rsp

    # The upper markdown text contains titles, abstracts, and categories of a series
    # of new papers on large language models, summarize these papers by topics, in each
    # category, give a concise summary and metion the titles of the referenced papers. 
    # Finally, give a summariztion of current researching trend in the end.