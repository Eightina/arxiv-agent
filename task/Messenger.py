import json
import requests
from enum import Enum

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

    

def sendMsg(webhook, body: MsgBody):
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data = body
    data = json.dumps(data)
    info = requests.post(url=webhook, data=data, headers=header)

if __name__ == "__main__":
    sendMsg(
        
    )