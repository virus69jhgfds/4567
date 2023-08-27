from concurrent.futures import ThreadPoolExecutor
#import alive
from aminoClass import *

user = {
    'email':
'Lord-najf30k58@wuuvo.com',
    'password':
    'kingzero159',
    'device':
    '1902483CD28DB37BBBFEA7192F556C1BAF9CB2FB65BD06EC431D858831579B1B7A588E71D607208F8B'
}

client = AminoClass(user["device"])

#لا تعدل في اي شي غير الي عليهم ملاحظات

print("Loged")
#سطر 12 رابط الجروب الي تهجم منه''
urlChat = 'http://aminoapps.com/p/a7ikcq'
#هنا في سطر 14 تحت رابط المنتديات بس ما تفصل بينهم غير بإنتر سطر جديد
urls ="""http://aminoapps.com/c/arabkpoper""".splitlines()

get = client.get_from_url(urlChat)
comId = get.comId
chatId = get.objectId

client2 = AminoClass("5265C5088493C6379E39C27AD5627962864F23F764BB7BCA5D26F5B9020561AB7C2D4B4A96D98B1897")
client2.login('pyv4u0q0wfJ3kuvf@wwjmp.com','159268370')
print("do")


def allOn(comId):
    start = 0
    users = []
    Num = client2.get_online_users(comId).userProfileCount
    leaders = client2.get_all_users(comId, "leaders").profile.userId
    curators = client2.get_all_users(comId, "curators").profile.userId
    hour = client2.get_leaderboard_info(comId, "hour", size=100).userId
    day = client2.get_leaderboard_info(comId, "day", size=100).userId
    rep = client2.get_leaderboard_info(comId, "rep", size=100).userId
    check = client2.get_leaderboard_info(comId, "check", size=100).userId
    quiz = client2.get_leaderboard_info(comId, "quiz", size=100).userId
    users.extend(leaders)
    users.extend(curators)
    users.extend(hour)
    users.extend(day)
    users.extend(rep)
    users.extend(check)
    users.extend(quiz)
    if len(str(Num)) < 3:
        dat = client2.get_online_users(comId, start=start,
                                       size=Num).profile.userId
        users.extend(dat)
    else:
        size = int(str(Num)[-2:])
        if size != 0:
            dat = client2.get_online_users(comId, start=start,
                                           size=size).profile.userId
            users.extend(dat)
            Num = Num - size
        while start < Num:
            dat = client2.get_online_users(comId, start=start,
                                           size=100).profile.userId
            users.extend(dat)
            start = start + 100
    print(f"number user in {comId}:{len(users)}")
    return users


def deleteCoHost():
    coHosts = client.get_chat_info(comId, chatId).coHosts
    for co in coHosts:
        client.deleteCoHost(comId, chatId, co)


def invite():
    try:
        print(
            client.inviteCoHost(comId, chatId, coHosts=users)['api:message'] +
            ":invited!")
        deleteCoHost()
    except Exception as e:
        deleteCoHost()
        print(e)
        pass


usersCom = []
for urlCom in urls:
    userCom = allOn(client.get_from_url(urlCom).comId)
    usersCom.append(userCom)

client.login(user['email'], user['password'])
while True:
    for users in usersCom:

        #try:invite()
        #except Exception as e:print(e)
        with ThreadPoolExecutor() as e:
            [e.submit(invite) for i in range(5)]
