import json
import warnings
import logging
from datetime import datetime, timedelta
import re
from outputMD import MDoutput
from accessLatestJSON import getRawPath 

# texts for logging
crawlURL = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=llm&terms-0-field=all&classification-computer_science=y&classification-eess=y&classification-mathematics=y&classification-physics_archives=all&classification-statistics=y&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"
emptyEntryWarningText = "\n============Warning==============>\nEmpty entry at idx: {}\n  Please access the site and locate the paper entry manually if you are interested:\n  " + crawlURL
failedScrawlWarningText = "\n============Warning==============>\nFailed to load page at idx: {}\n  Please access the paper entry manually if you are interested:\n  {}"
badFormatWarningText = "\n============Warning==============>\nBad date format at idx: {}\n  Please access the paper entry manually if you are interested:\n  {}\n  Adding entry to outdated paper set."
inDatedThreshold = 1 # criterion of whether the paper is in date

# task number and paths
rawDataFolderPath = "./output/raw"
currentDate = datetime.now().strftime("%Y-%m-%d")
logFile = f"./log/crawler_{currentDate}.log"
outputDir = "./output"


# date extraction
def extractDate(jsonRawDateString) -> datetime.date:
    months = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    pattern = r'(\d{1,2})\s(\w{3})\s(\d{4})'

    match = re.search(pattern, jsonRawDateString)
    if match:
        day = int(match.group(1))
        monthStr = match.group(2)
        year = int(match.group(3))
        month = months.get(monthStr)
        
        return datetime(year, month, day).date()
        
    else:
        return None

def isEntryInDated(entryDate:datetime.date) -> bool:
    today = datetime.now().date()
    date_difference = abs(today - entryDate)
    
    if (date_difference.days <= inDatedThreshold):
        return True
    else:
        return False

def outputEntriesMD(inDatedEntries, outDatedEntries, outputDir):
    if (len(inDatedEntries) > 0):
        today = datetime.now().date()
        MDoutput(inDatedEntries, outputDir + "/paper@{}.md".format(today))
        
    if (len(outDatedEntries.keys()) > 0):
        keys = list(outDatedEntries.keys())
        for key in keys:
            MDoutput(outDatedEntries[key], outputDir + "/outdated/paper@{}.md".format(key))


if __name__ == "__main__":
    
    # set log file
    with open(logFile, "w") as temp:
        pass
    logging.basicConfig(filename=logFile, level=logging.INFO)


    # read json file
    rawPath = getRawPath(rawDataFolderPath)
    with open(rawPath, "r") as raw:
        text = raw.read()
    jsonData = json.loads(text)
    logging.info("{} entries fetched from Arxiv".format(len(jsonData)))
    print("{} entries fetched from Arxiv".format(len(jsonData)))
    
    
    # results
    failedEntries = []
    inDatedEntries = []
    outDatedEntries = {}


    # processing json data in a loop
    for (idx, entry) in enumerate(jsonData):
        
        if (entry["arxiv_site"] == None):
            warnings.warn(emptyEntryWarningText.format(idx))
            logging.warning(emptyEntryWarningText.format(idx))
            continue
        
        if (entry["date"] == None or entry["date"] == ""):
            warnings.warn(failedScrawlWarningText.format(idx, entry["arxiv_site"]))
            logging.warning(failedScrawlWarningText.format(idx, entry["arxiv_site"]))
            failedEntries.append(entry["arxiv_site"])
            continue
        
        extractedEntryDate = extractDate(entry["date"])
        if (extractedEntryDate == None):
            warnings.warn(badFormatWarningText.format(idx, entry["arxiv_site"]))
            logging.warning(badFormatWarningText.format(idx, entry["arxiv_site"]))
            if ('badDateFormat' in outDatedEntries.keys()):
                outDatedEntries['outDatedEntries'].append(entry)
            else:
                outDatedEntries['outDatedEntries'] = [entry]
            continue
        
        isCurInDated = isEntryInDated(extractedEntryDate)
        if (not isCurInDated):
            if (extractedEntryDate in outDatedEntries.keys()):
                outDatedEntries[extractedEntryDate].append(entry)
            else:
                outDatedEntries[extractedEntryDate] = [entry]
            continue
                
        inDatedEntries.append(entry)
    
    # output data as md file
    outputEntriesMD(inDatedEntries, outDatedEntries, outputDir)