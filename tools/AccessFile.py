import os
import pickle
from markdown import markdown
import pdfkit
import json
from typing import List


def getRawPath(folderPath):
    # list all files
    files = os.listdir(folderPath)

    # initializing var for storing lastext json file and its mod time
    latestJson = None
    latestModificationTime = None

    # searching files as a loop
    for file in files:
        if file.endswith(".json"):
            filePath = os.path.join(folderPath[:-1], file)
            # get mod time
            modificationTime = os.path.getmtime(filePath)
            # if is newer
            if latestModificationTime is None or modificationTime > latestModificationTime:
                latestJson = filePath
                latestModificationTime = modificationTime

    # confirm if json file is found
    if latestJson:
        # print("find the latest json file:", latestJson)
        return latestJson
    else:
        return None

def loadOrCreateRecord(folderPath):
    # if exist then access
    filePath = folderPath + "paperdone.pkl"
    if os.path.exists(filePath):
        with open(filePath, 'rb') as file:
            data = pickle.load(file)
            return data
    # if not, create new one
    else:
        data = {}
        with open(filePath, 'wb') as file:
            pickle.dump(data, file)
        return data

def saveRecord(data, folderPath):
    filePath = folderPath + "paperdone.pkl"
    with open(filePath, 'wb') as file:
        pickle.dump(data, file)


def generate_markdown(data:List[dict]) -> str:
    markdown = ""
    for entry in data:
        markdown += f"## {entry['title']}\n"
        markdown += f"* Authors: {entry['authors']}\n"
        markdown += f"* Date: {entry['date']}\n"
        markdown += f"* Abstract: {entry['abstract']}\n"
        markdown += f"* Subjects: {entry['subjects']}\n"
        markdown += f"* [Link]({entry['arxiv_site']})\n\n"
    return markdown

def MDoutput(data:List[dict], outputPath:str) -> str:
    # 生成Markdown
    markdown_content = generate_markdown(data)

    # 将Markdown写入文件
    with open(outputPath, "w", encoding='UTF-8', errors='replace') as file:
        file.write(markdown_content)
    return markdown_content


def convertPDF(inputFile: str, outputFile: str, path_wk = r"/home/int.orion.que/dev/app/wkhtmltopdf/wkhtmltox/bin/wkhtmltopdf"):
    
    config = pdfkit.configuration(wkhtmltopdf=path_wk)

    # inputFile = folderPath + name + ".md"
    # outputFile = folderPath + name + ".pdf"
    
    with open(inputFile, "r") as f:
        html_text = markdown(f.read(), output_format="xhtml")

    # print(html_text)
    pdfkit.from_string(html_text, outputFile, configuration=config, options={'encoding': "UTF-8"})

        