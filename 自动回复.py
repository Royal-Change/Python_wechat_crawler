import itchat
import time


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
        msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
    else:
        msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    itchat.send_msg("{}收到好友@{}的信息：{}".format((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))),\
                                             msg_from,msg['Text']),toUserName='filehelper')
    return "[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的信息：{}\n".format(msg['Text'])


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == '自动回复':
    itchat.run()
