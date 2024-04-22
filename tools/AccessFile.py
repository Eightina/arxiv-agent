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

def loadOrCreateSet(folderPath):
    # 如果文件存在，则读取集合
    filePath = folderPath + "paperdone.pkl"
    if os.path.exists(filePath):
        with open(filePath, 'rb') as file:
            data = pickle.load(file)
            return data
    else:
        # 如果文件不存在，则创建一个新的集合
        data = set()
        with open(filePath, 'wb') as file:
            pickle.dump(data, file)
        return data

def saveSet(data, folderPath):
    filePath = folderPath + "paperdone.pkl"
    with open(filePath, 'wb') as file:
        pickle.dump(data, file)