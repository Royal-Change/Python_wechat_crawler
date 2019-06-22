import itchat
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


def sex_ratio():
    text = dict()
    friends = itchat.get_friends(update=True)[0:]
    male = "male"
    female = "female"
    other = "other"
    for i in friends[1:]:
        sex = i['Sex']
        if sex == 1:
            text[male] = text.get(male,0) + 1
        elif sex == 2:
            text[female] = text.get(female,0) + 1
        else:
            text[other] = text.get(other,0) + 1
    total = len(friends[1:])
    print("好友数量：{}".format(total))
    print("男性好友:{:.2f}%".format(float(text[male])/total*100) + "\n" +\
        "女性好友：{:.2f}%".format(float(text[female])/total*100) + "\n" +\
          "不明性别好友：{:.2f}%".format(float(text[other])/total*100))
    draw_pie(text, '朋友圈男女比例')


def draw_pie(date,tag=''):
    sex = [date['male'],date['female'],date['other']]
    labels = ['男','女','不明']
    colors = ['cornflowerblue','pink','lime']
    plt.pie(sex,labels=labels,colors=colors,autopct='%3.2f%%',labeldistance=1.1,pctdistance=0.8)
    plt.title('好友性别比例图')
    if tag == '':
        plt.savefig('扇形图.png')
    else:
        plt.savefig(tag+'扇形图.png')

if __name__ == '__main__':
    itchat.auto_login()
    sex_ratio()