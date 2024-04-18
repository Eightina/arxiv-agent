import json
from Logger import Logger, WarnLogger, InfoLogger
from datetime import datetime, timedelta
import re
from OutputMD import MDoutput
from AccessLatestJSON import getRawPath 
from enum import Enum, auto

# crawlURL = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=llm&terms-0-field=all&classification-computer_science=y&classification-eess=y&classification-mathematics=y&classification-physics_archives=all&classification-statistics=y&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"
class TaskSize(Enum):
    TINY = 25
    MID = 50
    BIG = 100
    LARGE = 200

class ArxivProcessor:   
    def __init__(self, inDatedThreshold = 1, rawDir = "./output/raw", outputDir =  "./output"): 
        self.crawlURL = f"\
            https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&\
            terms-0-term=llm&\
            terms-0-field=all&\
            classification-computer_science=y&classification-eess=y&\
            classification-mathematics=y&\
            classification-physics_archives=all&\
            classification-statistics=y&\
            classification-include_cross_list=include&\
            date-filter_by=all_dates&\
            date-year=&\
            date-from_date=&\
            date-to_date=&\
            date-date_type=submitted_date&\
            abstracts=show&\
            size={TaskSize.TINY}&\
            order=-announced_date_first\
            "

        self.inDatedThreshold = inDatedThreshold # criterion of whether the paper is in date

        # task number and paths
        self.rawDir = rawDir
        self.outputDir = outputDir

        # texts for logging
        self.emptyEntryWarningText = "\n============Warning==============>\nEmpty entry at idx: {}\n  Please access the site and locate the paper entry manually if you are interested:\n  " + self.crawlURL
        self.failedScrawlWarningText = "\n============Warning==============>\nFailed to load page at idx: {}\n  Please access the paper entry manually if you are interested:\n  {}"
        self.badFormatWarningText = "\n============Warning==============>\nBad date format at idx: {}\n  Please access the paper entry manually if you are interested:\n  {}\n  Adding entry to outdated paper set."

        self.failedEntries = []
        self.inDatedEntries = []
        self.outDatedEntries = {}

    # date extraction
    def extractDate(self, jsonRawDateString: str) -> datetime.date:
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

    def isEntryInDated(self, entryDate:datetime.date) -> bool:
        today = datetime.now().date()
        date_difference = abs(today - entryDate)
        
        if (date_difference.days <= self.inDatedThreshold):
            return True
        else:
            return False

    def outputEntriesMD(self, inDatedEntries, outDatedEntries, outputDir):
        if (len(inDatedEntries) > 0):
            today = datetime.now().date()
            MDoutput(inDatedEntries, outputDir + "/paper@{}.md".format(today))
            
        if (len(outDatedEntries.keys()) > 0):
            keys = list(outDatedEntries.keys())
            for key in keys:
                MDoutput(outDatedEntries[key], outputDir + "/outdated/paper@{}.md".format(key))


    def process(self):
        logFile = Logger.newLogFile()
        warner = WarnLogger(logFile)
        infoer = InfoLogger(logFile)

        # read json file
        rawPath = getRawPath(self.rawDir)
        with open(rawPath, "r") as raw:
            text = raw.read()
        jsonData = json.loads(text)
        infoer.log("{} entries fetched from Arxiv".format(len(jsonData)))
        print("{} entries fetched from Arxiv".format(len(jsonData)))
        
        
        # processing json data in a loop
        for (idx, entry) in enumerate(jsonData):
            
            if (entry["arxiv_site"] == None):
                warner.log(self.emptyEntryWarningText.format(idx))
                continue
            
            if (entry["date"] == None or entry["date"] == ""):
                warner.log(self.failedScrawlWarningText.format(idx, entry["arxiv_site"]))
                self.failedEntries.append(entry["arxiv_site"])
                continue
            
            extractedEntryDate = self.extractDate(entry["date"])
            if (extractedEntryDate == None):
                warner.log(self.badFormatWarningText.format(idx, entry["arxiv_site"]))
                if ('badDateFormat' in self.outDatedEntries.keys()):
                    self.outDatedEntries['outDatedEntries'].append(entry)
                else:
                    self.outDatedEntries['outDatedEntries'] = [entry]
                continue
            
            isCurInDated = self.isEntryInDated(extractedEntryDate)
            if (not isCurInDated):
                if (extractedEntryDate in self.outDatedEntries.keys()):
                    self.outDatedEntries[extractedEntryDate].append(entry)
                else:
                    self.outDatedEntries[extractedEntryDate] = [entry]
                continue
                    
            self.inDatedEntries.append(entry)
        
            # output data as md file
        self.outputEntriesMD(self.inDatedEntries, self.outDatedEntries, self.outputDir)
        return self.inDatedEntries

if __name__ == "__main__":
    processor = ArxivProcessor()
    processor.process()