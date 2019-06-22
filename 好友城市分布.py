import itchat
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


def parse_friends():
    citys = dict()
    friends = itchat.get_friends(update=True)[0:]
    for i in friends[1:]:
        city = (i['Province'] +"\n"+ i['City']).replace(" ","\n").replace("-","\n")
        citys[city] = citys.get(city,0) + 1
    draw_plot(citys, '微信好友城市分布')


def draw_plot(data,tag=''):
    plt.figure(figsize=(20,8))
    cityList = []
    cityNum = []
    for i in sorted(data,key=data.__getitem__,reverse=True):
        cityList.append(i)
        cityNum.append(data[i])
    plt.bar(range(len(data)),cityNum,alpha=0.8)
    plt.xticks(range(len(data)),cityList,size='small',rotation=30)
    for x,y in zip(range(len(data)),cityNum):
        plt.text(x,y,y,ha='center',va='bottom')
    plt.xlabel('城市')
    plt.ylabel('数量')
    plt.title('好友城市分布图')
    if tag == '':
        plt.savefig('柱状图.png')
    else:
        plt.savefig(tag+'柱状图.png')


if __name__ == '__main__':
    itchat.auto_login()
    parse_friends()