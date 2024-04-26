import os
import pickle

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