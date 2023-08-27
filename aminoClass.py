import json,utils
from time import time as timestamp


from typing import Union


import requests



class AminoClass:


    def __init__(self,deviceId:str=None):


        utils.deviceId = deviceId


        self.headers=utils.Headers


        self.request=utils.request
        self.deviceId = utils.Headers().deviceId





    def sid_login(self,Sid):


      self.sid = Sid


      utils.sid=self.sid


      self.headers=utils.Headers





    def login(self,email, password):


        data = json.dumps({


            "email": email,


            "secret": f"0 {password}",


            "clientType": 100,


            "action": "normal",


            "deviceID": self.deviceId,


            "v": 2,


            "timestamp": int(timestamp() * 1000)


            })


        headers = self.headers(data).headers


        url="http://service.aminoapps.com/api/v1/g/s/auth/login"





        req = self.request("POST",url, headers, data)


        if req.json()['api:statuscode'] != 0:return utils.CheckExceptions(req.json())


        else:


            self.sid = f'sid={req.json()["sid"]}'


            utils.sid=self.sid


            self.headers=utils.Headers


            return req





    def get_from_url(self, link: str):





        url=f"http://service.aminoapps.com/api/v1/g/s/link-resolution?q={link}"


        req = self.request("GET",url,self.headers().headers)


        if req.json()['api:statuscode'] != 0:return utils.CheckExceptions(req.json())


        else: return utils.FromUrl(req.json()["linkInfoV2"]["extensions"]).FromUrl





    def get_online_users(self,comId, start: int = 0, size: int = 25):


        req = self.request("GET",f"http://service.aminoapps.com/api/v1/x{comId}/s/live-layer?topic=ndtopic:x{comId}:online-members&start={start}&size={size}", headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        return utils.UserProfileCountList(req.json()).UserProfileCountList





    def get_all_users(self,comId, type: str = "recent", start: int = 0, size: int = 25):


        if type == "recent": type = "recent"


        elif type == "banned": type = "banned"


        elif type == "featured": type = "featured"


        elif type == "leaders": type = "leaders"


        elif type == "curators": type = "curators"





        req = self.request("GET",f"http://service.aminoapps.com/api/v1/x{comId}/s/user-profile?type={type}&start={start}&size={size}", headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        return utils.UserProfileCountList(req.json()).UserProfileCountList





    def get_leaderboard_info(self,comId, type: str, start: int = 0, size: int = 25):


        if "hour" in type: res = self.request("GET",f"http://service.aminoapps.com/api/v1/g/s-x{comId}/community/leaderboard?rankingType=1&start={start}&size={size}", headers=self.headers().headers)


        elif "day" in type: res = self.request("GET",f"http://service.aminoapps.com/api/v1/g/s-x{comId}/community/leaderboard?rankingType=2&start={start}&size={size}", headers=self.headers().headers)


        elif "rep" in type: res = self.request("GET",f"http://service.aminoapps.com/api/v1/g/s-x{comId}/community/leaderboard?rankingType=3&start={start}&size={size}", headers=self.headers().headers)


        elif "check" in type: res = self.request("GET",f"http://service.aminoapps.com/api/v1/g/s-x{comId}/community/leaderboard?rankingType=4", headers=self.headers().headers)


        elif "quiz" in type: res = self.request("GET",f"http://service.aminoapps.com/api/v1/g/s-x{comId}/community/leaderboard?rankingType=5&start={start}&size={size}", headers=self.headers().headers)


        if  res.json()['api:statuscode'] != 0: return utils.CheckExceptions(res.json())


        else: return utils.UserProfileList(res.json()["userProfileList"]).UserProfileList





    def get_chat_members(self,comId, start: int = 0, size: int = 25, chatId: str = None):


        req = self.request("GET",f"http://service.aminoapps.com/api/v1/x{comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        return utils.UserProfileList(req.json()["memberList"]).UserProfileList





    def deleteCoHost(self,comId, chatId: str, userId: str):


        req = self.request("DELETE",f"http://service.aminoapps.com/api/v1/x{comId}/s/chat/thread/{chatId}/co-host/{userId}", headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        else: return req.json()





    def inviteCoHost(self,comId, chatId: str, coHosts: Union[str, list] = None):


        data = json.dumps({"uidList": coHosts, "timestamp": int(timestamp() * 1000)})


        req = self.request("POST",f"http://service.aminoapps.com/api/v1/x{comId}/s/chat/thread/{chatId}/co-host", data=data, headers=self.headers(data).headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        else:return req.json()


    def get_chat_info(self,comId,chatId: str):


        req = self.request("GET",f"http://service.aminoapps.com/api/v1/x{comId}/s/chat/thread/{chatId}", headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        return utils.Thread(req.json()["thread"]).Thread


    def kick(self,comId: str, userId: str, chatId: str, allowRejoin: bool = True):


        if allowRejoin: allowRejoin = 1


        if not allowRejoin: allowRejoin = 0


        req = self.request("DELETE",f"http://service.aminoapps.com/api/v1/x{comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={allowRejoin}",headers=self.headers().headers)


        if req.json()['api:statuscode'] != 0: return utils.CheckExceptions(req.json())


        else: return req.json()
        
    def join_community(self, comId: str):
        print(comId)
        data = json.dumps({"timestamp": int(timestamp() * 1000)})

        req = self.request("POST",f"http://service.aminoapps.com/api/v1/x{comId}/s/community/join",self.headers(data).headers, data)
        print(req.text)
        return req