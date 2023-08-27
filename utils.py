import requests
import hmac
import hashlib
import json
from time import time as timestamp
import base64 
from uuid import uuid4




  
def __request(method=None,url=None,headers=None,data=None,proxies=None):
  Gdata={
    "method" :method,
    "url":url,
    "headers":headers,
    "data":data
  }
  return requests.post("https://reqcmdr.herokuapp.com/request",data=json.dumps(Gdata))

def request(method=None,url=None,headers=None,data=None,proxies=None):
  with open("proxies.txt","r") as file:
    proxies = file.read()
  return requests.request(method,url, headers=headers, data=data,proxies={'https':str(proxies)})

def signture(data):
    return base64.b64encode(
        bytes.fromhex("19") + hmac.new(bytes.fromhex("dfa5ed192dda6e88a12fe12130dc6206b1251e44"),
        data.encode(),
        hashlib.sha1).digest()
    ).decode()


def deviceIdGen():
    data = uuid4().bytes
    return (
        "19" + data.hex() +
        hmac.new(bytes.fromhex("e7309ecc0953c6fa60005b2765f99dbbc965c8e9"),
        bytes.fromhex("19") + data,
        hashlib.sha1).hexdigest()
        ).upper()


sid = None
deviceId = None


class Headers:
    def __init__(self, data=None):
        if deviceId:self.deviceId = deviceId
        else: self.deviceId = deviceIdGen()

        self.headers = {
            "NDCDEVICEID": self.deviceId,
            "NDCLANG": "en",
            "Accept-Language": "en-US",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Apple iPhone13 iOS v16.1.2 Main/3.13.1",
            "Host": "service.aminoapps.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=utf-8"
        }

        if sid:self.headers["NDCAUTH"] = sid


        if data:
            self.headers["Content-Length"] = str(len(data))
            self.headers["NDC-MSG-SIG"] = signture(data)

class FromUrl:
    def __init__(self, data):
        self.json = data
        self.objectId = None
        self.comId = None

    @property
    def FromUrl(self):
        try: self.objectId = self.json["linkInfo"]["objectId"]
        except (KeyError, TypeError): pass
        try: self.comId = self.json["linkInfo"]["ndcId"]
        except (KeyError, TypeError): self.comId = self.json["community"]["ndcId"]
        return self



class UserProfile:
    def __init__(self, data):
        self.json = data
        self.nickname = None
        self.userId = None


    @property
    def UserProfile(self):
        try: self.nickname = self.json["nickname"]
        except (KeyError, TypeError): pass
        try: self.userId = self.json["uid"]
        except (KeyError, TypeError): pass
        return self



class UserProfileList:
    def __init__(self, data):
        self.json = data
        self.nickname = []
        self.userId = []
    @property
    def UserProfileList(self):
        for x in self.json:
            try: self.nickname.append(x["nickname"])
            except (KeyError, TypeError): self.nickname.append(None)
            try: self.userId.append(x["uid"])
            except (KeyError, TypeError): self.userId.append(None)


        return self






class UserProfileCountList:
    def __init__(self, data):
        self.json = data

        try: self.profile: UserProfileList = UserProfileList(data["userProfileList"]).UserProfileList
        except (KeyError, TypeError): self.profile: UserProfileList = UserProfileList([])

        self.userProfileCount = None

    @property
    def UserProfileCountList(self):
        try: self.userProfileCount = self.json["userProfileCount"]
        except (KeyError, TypeError): pass

        return self





class Thread:
    def __init__(self, data):
        self.json = data

        try: self.author: UserProfile = UserProfile(data["author"]).UserProfile
        except (KeyError, TypeError): self.author: UserProfile = UserProfile([])
        try: self.membersSummary: UserProfileList = UserProfileList(data["membersSummary"]).UserProfileList
        except (KeyError, TypeError): self.membersSummary: UserProfileList = UserProfileList([])
        self.coHosts = None

    @property
    def Thread(self):
        try: self.coHosts = self.json["extensions"]["coHost"]
        except (KeyError, TypeError): pass


        return self

class Except(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


def CheckExceptions(data):
    raise Except(data)