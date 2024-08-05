import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tools.Logger import Logger, WarnLogger, InfoLogger

class ArxivCrawler:
    def __init__(self, url: str, warner: WarnLogger, infoer: InfoLogger, outputDir="./output/raw/"):
        if not url:
            raise ValueError("no url")
        if not warner or not infoer:
            raise ValueError("no logger")
        self.url = url
        self.warner = warner
        self.infoer = infoer
        self.outputDir = outputDir
        self.jsonRes = []


    def fetchURL(self, url, retries=3, backoff_factor=0.3, timeout=5):
        
        session = requests.Session()
        retryStrategy = Retry(
            total=retries,
            backoff_factor=backoff_factor, # sleep_time = backoff_factor * (2 ** (retry_attempt - 1))
            status_forcelist=[500, 502, 503, 504, 429],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retryStrategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()  # raise an exception for 4xx and 5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            self.warner.log(f"Crawler failing when fetching URL: {e}")
            return None


    def crawlArxivPage(self):

        response = self.fetchURL(self.url)
        if (not response):
            self.warner.log(f"Crawler receiving no response when requesting {self.url}")
            raise ValueError(f"Crawler receiving no response when requesting {self.url}")
        soup = BeautifulSoup(response.content, "html.parser")

        papers_url = []
        resolved = soup.find_all("p", class_="list-title is-inline-block")
        for paper in resolved:
            paper_url = paper.find_all("a")[0]['href']
            papers_url.append(paper_url)
        
        for (i, paper_url) in enumerate(papers_url):
            self.infoer.log("Crawler fetching page {} / {} in total".format(i, len(papers_url)))
            cur_date = cur_title = cur_authors = cur_abstract = cur_subjects = ""
            cur_response = self.fetchURL(paper_url)
            if (cur_response):
                cur_soup = BeautifulSoup(cur_response.content, "html.parser")
                cur_date = cur_soup.find("div", class_="dateline").text.strip()
                cur_title = cur_soup.find("h1", class_="title mathjax").text
                cur_authors = cur_soup.find("div", class_="authors").text
                cur_abstract = cur_soup.find("blockquote", class_="abstract mathjax").text.strip()
                cur_subjects = cur_soup.find("td", class_="tablecell subjects").text.strip()
                cur_filelink = "https://arxiv.org" + cur_soup.find("a", class_="abs-button download-pdf")['href']
            else:
                self.warner.log(f"Crawler skipping index {i} @ {paper_url}")
            self.jsonRes.append({
                "arxiv_site": paper_url,
                "date": cur_date,
                "title": cur_title,
                "authors": cur_authors,
                "abstract": cur_abstract,
                "subjects": cur_subjects,
                "file_link": cur_filelink
            })
            time.sleep(random.uniform(0.01, 0.05))

        return self.jsonRes


    def saveToJSON(self, data, filePath):
        with open(filePath, "w") as f:
            json.dump(data, f, indent=4)
        self.infoer.log(f"Crawler saving json to {filePath}")

    def crawlToJSON(self):
        self.crawlArxivPage()
        currentDate = datetime.now().strftime("%Y-%m-%d")
        jsonFile = f"crawler_{currentDate}.json"
        self.saveToJSON(self.jsonRes, self.outputDir + jsonFile)
        

if __name__ == "__main__":
    crawlURL = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=llm&terms-0-field=all&classification-computer_science=y&classification-eess=y&classification-mathematics=y&classification-physics_archives=all&classification-statistics=y&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"
    crawler = ArxivCrawler(crawlURL)
    crawler.crawlToJSON()