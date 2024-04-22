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
    
    def __init__(self, key="1cb2d8e5-acd9-4d75-ae5f-2d08d0f89044"):
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
        # url为群组机器人WebHook，配置项
        # url = self.tarURL
        # params = parse.parse_qs( parse.urlparse( url ).query )
        # webHookKey=params['key'][0]
        # upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={self.key}&type=file'
        headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
        # filename = os.path.basename(filePath)
        try:
            multipart = MultipartEncoder(
                fields={'filename': filePath, 'filelength': '', 'name': 'media', 'media': (filePath, open(filePath, 'rb'), 'application/octet-stream')},
                boundary='-------------------------acebdf13572468')
            headers['Content-Type'] = multipart.content_type
            resp = requests.post(self.fileURL, headers=headers, data=multipart)
            json_res = resp.json()
            if json_res.get('media_id'):
                print(f"企业微信机器人上传文件成功，file:{filePath}")
                return json_res.get('media_id')
        except Exception as e:
            # print(f"企业微信机器人上传文件失败，file: {filepath}, 详情：{e}")
            print("企业微信机器人上传文件失败,详细信息:" + str(e))
            return ""

        # headers = {
        #     'Content-Type': 'multipart/form-data',
        # }

        # # params = (
        # #     ('key', self.key) # webhookurl key
        # #     ('type', 'file')
        # # )        
        
        # with open(filePath, 'rb') as f:
            
        #     files = {
        #         'filename': filePath,
        #         'name' : "media",
        #         'Content-Disposition': 'form-data',
        #         'Content-Type': 'application/octet-stream',
        #         'file': (filePath, f, 'application/octet-stream'),
        #         'boundary': "acebdf13572468"
        #     }
        #     formData = MultipartEncoder(files)  # format transforming
        #     # headers['Content-type'] = formData.content_type
        #     # headers["boundary"] = formData.boundary_value
        #     headers['Content-Length'] = str(formData.len)
            
        #     r = requests.post(self.fileURL , data=formData, headers=headers)    # 请求

        #     media_id = r.json()['media_id']
        #     logger.debug(str(r.json()))
        #     logger.debug(str(media_id))
        #     return media_id

# if __name__ == "__main__":
#     msger = Messenger()
# b'{"errcode":40058,"errmsg":"invalid param \'key\', hint: [1713777111197560034674942], from ip: 139.227.220.7, more info at https://open.work.weixin.qq.com/devtool/query?e=40058"}'
# {'Date': 'Mon, 22 Apr 2024 09:11:51 GMT', 'Content-Type': 'application/json; charset=UTF-8', 'Content-Length': '175', 'Connection': 'keep-alive', 'Server': 'nginx', 'Error-Code': '40058', 'Error-Msg': "invalid param 'key', hint: [1713777111197560034674942], from ip: 139.227.220.7, more info at https://open.work.weixin.qq.com/devtool/query?e=40058", 'X-W-No': '5'}