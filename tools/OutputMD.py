import json
from typing import List

def generate_markdown(data:List[dict]):
    markdown = ""
    for entry in data:
        markdown += f"## {entry['title']}\n"
        markdown += f"* Authors: {entry['authors']}\n"
        markdown += f"* Date: {entry['date']}\n"
        markdown += f"* Abstract: {entry['abstract']}\n"
        markdown += f"* Subjects: {entry['subjects']}\n"
        markdown += f"* [Link]({entry['arxiv_site']})\n\n"
    return markdown

def MDoutput(data:List[dict], outputPath:str):
    # 生成Markdown
    markdown_content = generate_markdown(data)

    # 将Markdown写入文件
    with open(outputPath, "w", encoding='gbk', errors='replace') as file:
        file.write(markdown_content)
