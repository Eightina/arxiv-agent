import json
import requests
from requests_toolbelt import MultipartEncoder
from enum import Enum
from metagpt.logs import logger
from urllib import parse

class MsgBody(Enum):
    TX = {
        "msgtype": "text",
        "text": {
            "content": "{content}"
        }
    }

    IM = {
        "msgtype": "image",
        "image": {
            "base64": "{content}",
            "md5": "{MD5}"
        }
    }

    MD = {
        "msgtype": "markdown",
        "markdown": {
            "content": "{content}"
        }
    }
    
    FL = {
        "msgtype": "file",
        "file": {
            "media_id": "{content}"
        }
    }

# https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1cb2d8e5-acd9-4d75-ae5f-2d08d0f89044
class Messenger:
    
    def __init__(self, key):
        self.key = key
        self.tarURL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(self.key) 
        self.fileURL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={}&type=file&debug=1".format(self.key)
        
    def sendMsg(self, body: MsgBody):
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        data = body
        data = json.dumps(data)
        info = requests.post(url=self.tarURL, data=data, headers=header)
        logger.info(str(info.json()))
        return info

    def fileup(self, filePath):        
    # get media_id
        id_url = self.fileURL
        files = {'file': open(filePath, 'rb')}
        res = requests.post(url=id_url, files=files)
        media_id = res.json()['media_id']
        return media_id