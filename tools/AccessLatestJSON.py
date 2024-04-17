import os

def getRawPath(folderPath):
    # list all files
    files = os.listdir(folderPath)

    # initializing var for storing lastext json file and its mod time
    latestJson = None
    latestModificationTime = None

    # searching files as a loop
    for file in files:
        if file.endswith(".json"):
            filePath = os.path.join(folderPath, file)
            # get mod time
            modificationTime = os.path.getmtime(filePath)
            # if is newer
            if latestModificationTime is None or modificationTime > latestModificationTime:
                latestJson = filePath
                latestModificationTime = modificationTime

    # 确认是否找到了 JSON 文件
    if latestJson:
        # print("找到最新的 JSON 文件:", latestJson)
        return latestJson
    else:
        return None
    