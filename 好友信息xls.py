import itchat
import xlwt
import re


def write_info(single_list,j,table):
    i = 0
    for each in single_list:
        table.write(j,i,each)
        i += 1


def fri_info():
    friends = itchat.get_friends(update=True)[1:]
    file = xlwt.Workbook(encoding = 'utf-8')
    table = file.add_sheet('sheet 1')
    header = ["微信名", "备注名", "性别", "签名", "省份", "城市"]
    for i in range(6):
        table.write(0,i,header[i])
    j = 1
    for i in friends[1:]:
        allFri = []
        nick_nmae = i['NickName']
        if i['Sex'] == 1:
            sex = '男'
        elif i['Sex'] == 2:
            sex = '女'
        else:
            sex = '不明'
        remark_name = i['RemarkName']
        sigNature = i['Signature'].strip().replace("span","").replace("class","").replace("emoji","")
        rep = re.compile("1f/d+/w*|[<>/=]")
        sigNature = rep.sub("", sigNature)
        province = i['Province']
        city = i['City']
        allFri.extend([nick_nmae,remark_name,sex,sigNature,province,city])
        write_info(allFri,j,table)
        j += 1
    file.save('微信好友信息.xls')

if __name__ == '__main__':
    itchat.auto_login()
    fri_info()

