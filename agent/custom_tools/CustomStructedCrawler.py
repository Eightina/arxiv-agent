# from enum import Enum, auto
# from tools.Logger import Logger, WarnLogger, InfoLogger
# from tools.Crawler import ArxivCrawler
# from tools.DataProcessor import ArxivProcessor

# from metagpt.tools.tool_registry import register_tool


# class TaskSize(Enum):
#     TINY = 25
#     MID = 50
#     BIG = 100
#     LARGE = 200
    
# url = f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&\
#     terms-0-term=llm&\
#     terms-0-field=all&\
#     classification-computer_science=y&classification-eess=y&\
#     classification-mathematics=y&\
#     classification-physics_archives=all&\
#     classification-statistics=y&\
#     classification-include_cross_list=include&\
#     date-filter_by=all_dates&\
#     date-year=&\
#     date-from_date=&\
#     date-to_date=&\
#     date-date_type=submitted_date&\
#     abstracts=show&\
#     size={TaskSize.TINY.value}&\
#     order=-announced_date_first\
#     ".replace(' ','')

# @register_tool()
# def CustomStructedCrawler() -> str:
#     """
#     Specialized crawler that can crawl Arxiv.com to fetch the latest
#     Large Language Model related papers' links, dates, titles, authors,
#     abstracts, and subjects, and then return these results as string in
#     markdown format
#     """
#     logFile = Logger.newLogFile()
#     warner = WarnLogger(logFile)
#     infoer = InfoLogger(logFile)
#     crawler = ArxivCrawler(url, warner, infoer)
#     crawler.crawlToJSON()
#     processor = ArxivProcessor(url, warner, infoer)
#     mdstring = processor.process()
#     return mdstring
    
# if __name__ == "__main__":
#     pass