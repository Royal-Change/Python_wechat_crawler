import itchat,re,time


@itchat.msg_register(itchat.content.FRIENDS)
def auto_accept_friends(msg):
    req = re.compile(keyword)
    if req.search(msg['RecommendInfo']['Content'],re.IGNORECASE):
        if msg['RecommendInfo']['Sex'] == 1:
            sex = '男'
        elif msg['RecommendInfo']['Sex'] == 2:
            sex = '女'
        else:
            sex = '不明'
        itchat.add_friend(**msg['Text'])
        itchat.send_msg('我已添加你为好友。',toUserName=msg['RecommendInfo']['UserName'])
        itchat.send_msg(
            "{}收到@{}（{}）的好友请求：{}".format((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))), \
                                     msg['RecommendInfo']['NickName'], sex, msg['RecommendInfo']['Content']), toUserName='filehelper')


if __name__ == '__main__':
    itchat.auto_login()
    keyword = input("请输入接受好友时，好友请求中包含的关键词：").replace("\n","")
    if keyword != "":
        itchat.run()
    else:
        print("请输入不为空的关键字！")

if __name__ == '自动添加好友':
    keyword = input("请输入接受好友时，好友请求中包含的关键词：").replace("\n","")
    if keyword is not None:
        itchat.run()
    else:
        print("请输入不为空的关键字！")
