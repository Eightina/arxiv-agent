import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime

outputDir = "./output/raw/"

def crawl_arxiv_page():
    url = f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=llm&terms-0-field=all&classification-computer_science=y&classification-eess=y&classification-mathematics=y&classification-physics_archives=all&classification-statistics=y&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")


    # for entry in soup.find_all("div", class_="list-title mathjax"):
    #     title = entry.text.strip()
    #     abstract_id = entry.find_next("div", class_="list-identifier")
    #     abstract_url = abstract_id.find_next("a")["href"]
    #     abstract = get_abstract(abstract_url)
    #     papers.append({"title": title, "abstract": abstract})
    papers_url = []
    resolved = soup.find_all("p", class_="list-title is-inline-block")
    for paper in resolved:
        paper_url = paper.find_all("a")[0]['href']
        papers_url.append(paper_url)
    
    json_res = []
    for (i, paper_url) in enumerate(papers_url):
        print("fetching page {} / {} in total".format(i, len(papers_url)))
        cur_response = requests.get(paper_url)
        cur_soup = BeautifulSoup(cur_response.content, "html.parser")
        cur_date = cur_soup.find("div", class_="dateline").text.strip()
        cur_title = cur_soup.find("h1", class_="title mathjax").text
        cur_authors = cur_soup.find("div", class_="authors").text
        cur_abstract = cur_soup.find("blockquote", class_="abstract mathjax").text.strip()
        cur_subjects = cur_soup.find("td", class_="tablecell subjects").text.strip()
        json_res.append({
            "arxiv_site": paper_url,
            "date": cur_date,
            "title": cur_title,
            "authors": cur_authors,
            "abstract": cur_abstract,
            "subjects": cur_subjects
        })
        time.sleep(random.uniform(0.01, 0.05))

    return json_res


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def main():
    papers = crawl_arxiv_page()
    currentDate = datetime.now().strftime("%Y-%m-%d")
    jsonFile = f"crawler_{currentDate}.json"
    save_to_json(papers, outputDir + jsonFile)

if __name__ == "__main__":
    main()