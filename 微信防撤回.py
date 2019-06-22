import itchat
import re
import time
from itchat.content import *

msg_dict = {}
face_bug = None


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=True)
def handle_receive_msg(msg):
    global face_bug
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if 'ActualNickName' in msg:
        group_name = itchat.get_chatrooms(update=True)
        for g in group_name:
            if '兼职' not in g['NickName']:
                if msg['FromUserName'][0] == g['UserName'][0]:
                    group_name = g['NickName']
                    break
            else:
                return 0
            print(group_name)
        msg_from = msg['ActualNickName']
        friends = itchat.get_friends(update=True)
        for f in friends:
            if msg_from == f['UserName']:
                if f['RemarkName']:
                    msg_from = f['RemarkName']
                else:
                    msg_from = f['NickName']
    else:
        if itchat.se0arch_friends(userName=msg['FromUserName'])['RemarkName']:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        group_name = None
    msg_id = msg['MsgId']
    msg_time = msg['CreateTime']
    msg_content = None
    msg_share_url = None

    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' or msg['Type'] == 'Attachment' or msg['Type'] == 'Video':
        msg_content = msg['FileName']  # 内容就是他们的文件名
    elif msg['Type'] == 'Picture':
        p = re.compile('cdnurl = \"(.*?/)\"')
        if p.search(msg['Content']) is not None:
            msg_content = p.search(msg['Content']).group(1)
        else:
            msg_content = msg['FileName']
        print(msg)
    elif msg['Type'] == 'Card':
        msg_content = msg['RecordingInfo']['RemarkName'] + r" 的名片"  # 内容就是推荐人的昵称和性别
        if msg['RecordingInfo']['Sex'] == 1:
            msg_content += ",性别：男"
        elif msg['RecordingInfo']['Sex'] == 2:
            msg_content += ",性别：女"
        else:
            msg_content += "，性别：不明"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,
                                                                                                                    2,
                                                                                                                    3)
        if not location:
            msg_content = r"纬度->" + x.__str__() + r"经度->" + y.__str__()
        else:
            msg_content = location
    elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content

    msg_dict.update({
        msg_id: {
            "msg_from": msg_from, "msg_time": msg_time,
            "msg_time_rec": msg_time_rec, "msg_type": msg['Type'],
            "msg_content": msg_content, "msg_share_url": msg_share_url,
            "group_name": group_name
        }
    })

    del_info = []
    for k in msg_dict:
        m_time = msg_dict[k]['msg_time']
        if time.time() - m_time > 90:
            del_info.append(k)
        if del_info:
            for i in del_info:
                del msg_dict[i]


@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True)
def send_msg_helper(msg):
    global face_bug
    msgC = msg['Content'].replace("&lt;", "<").replace("&gt;", ">")
    if re.search("\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msgC) is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msgC).group(1)
        old_msg = msg_dict.get(old_msg_id)
        if len(old_msg_id) < 11:
            itchat.send_file(face_bug, toUserName='filehelper')
        else:
            msg_body = old_msg.get('msg_from') + " " + old_msg.get('msg_time_rec') + " 撤回了" + old_msg.get(
                'msg_type') + "消息:" + "\n" \
                       + old_msg['msg_content']
            if old_msg.get('group_name') is not None:
                msg_body = "群聊" + old_msg.get('group_name') + "的" + msg_body
            if old_msg['msg_type'] == 'Sharing':
                msg_body += "\n这个链接->" + old_msg.get('msg_share_url')
            itchat.send(msg_body, toUserName='filehelper')
            if old_msg['msg_type'] == 'Picture' or old_msg['msg_type'] == 'Recording' \
                    or old_msg['msg_type'] == 'Video' or old_msg['msg_type'] == 'Attachment':
                file = "@fil@{}".format(old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
        msg_dict.pop(old_msg_id)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == '微信防撤回':
    itchat.run()
