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

    # 在原文中标注每篇论文具体所属的主题，可能是以下任意一种：
class Taxonomize(Action):
    PROMPT_TEMPLATE: str = """
    {}
    上述文本包含了一系列最新的大语言模型领域的论文的标题，摘要等内容。
    对每篇论文进行分类，可能是以下任意一个主题：
    模型架构与性能优化，模型创新应用，模型评估与数据集，模型隐私与安全，模型公平与可解释性，其他
    """
    #

    name: str = "Taxonomize"

    async def run(self, mdstring: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(mdstring)
        rsp = await self._aask(prompt)
        # logger.debug("====================Taxonomize======================\n" + str(type(prompt)))
        # logger.debug("====================Taxonomize======================\n" + str(type(mdstring)))
        # logger.debug("====================Taxonomize======================\n" + str(type(mdstring[0])))
        return mdstring + rsp

    
class Summarize(Action):
    PROMPT_TEMPLATE: str = """
    {}
    上述文本包含了一系列最新的大语言模型领域的论文的标题，摘要，主题（模型架构与性能优化，模型创新应用，模型评估与数据集，模型隐私与安全，模型公平与可解释性，其他）等内容。
    使用中文，将相同主题的文章放在一起，并分析每篇文章解决的问题与方法论。
    最后总结当前大语言模型领域研究的最新趋势，突出重点。
    """
    #

    name: str = "Summarize"

    async def run(self, mdstring: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(mdstring) #???????mdstring is a list????????
        logger.info("====================Summarize->mdstring======================\n" + str(prompt))
        rsp = await self._aask(prompt)
        logger.info("====================Summarize->rsp======================\n"+str(len(rsp)))

        return rsp

    # The upper markdown text contains titles, abstracts, and categories of a series
    # of new papers on large language models, summarize these papers by topics, in each
    # category, give a concise summary and metion the titles of the referenced papers. 
    # Finally, give a summariztion of current researching trend in the end.