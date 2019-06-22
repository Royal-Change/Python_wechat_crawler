import itchat, time

try:
    if itchat.load_login_status(fileDir='itchat.pkl'):
       pass
    else:
        print("请扫描二维码登录微信：")
        time.sleep(1)
        itchat.auto_login(hotReload=True)

    print("1、男女性别比例扇形图\n" +
          "2、好友城市分布柱状图\n" +
          "3、个性签名词云图\n" +
          "4、微信自动回复\n" +
          "5、自动添加好友\n" +
          "6、微信防撤回\n" +
          "7、微信好友信息表格\n" +
          "8、退出登录")
    num = input("请输入所需功能对应的编号，例如 ‘3’：")
    if num == '1':
        obj = __import__('男女性别比例')
        obj.sex_ratio()
    elif num == '2':
        obj = __import__('好友城市分布')
        obj.parse_friends()
    elif num == '3':
        obj = __import__('词云')
        obj.signature()
    elif num == '4':
        obj = __import__('自动回复')
    elif num == '5':
        obj = __import__('自动添加好友')
    elif num == '6':
         obj = __import__('微信防撤回')
    elif num == '7':
        obj = __import__('好友信息xls')
        obj.fri_info()
    elif num == '8':
        itchat.logout()
    else:
        print("请输入1—8的数字！")
except:
    print("system error")