import itchat
from wordcloud import WordCloud
import jieba
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import re


def signature():
    sig_list = []
    signature_path = 'signature.txt'
    friends = itchat.get_friends(update=True)[1:]
    for i in friends:
        signature = i['Signature'].strip().replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("(1f\d+\w*)|[<>/=]")
        signature = rep.sub("", signature)
        sig_list.append(signature)
    text = "".join(sig_list)
    with open(signature_path, "w", encoding='utf-8') as f:
        word_list = jieba.lcut(text, cut_all=True)
        word_space_split = " ".join(word_list)
        f.write(word_space_split)
        f.close()
    draw_wordcloud(signature_path, u'朋友圈签名')


def draw_wordcloud(path, tag=''):
    f = open(path, 'r', encoding='utf-8').read()
    cut_text = "".join(jieba.lcut(f))
    coloring = np.array(Image.open('cat.jpg'))
    wc = WordCloud(font_path='C:\\Windows\\Fonts\\simhei.ttf', background_color="white", mask=coloring, max_words=2000,
                   scale=2).generate(cut_text)
    plt.imshow(wc)
    plt.axis("off")
    if tag == '':
        wc.to_file("词云.png")
    else:
        wc.to_file(tag + "词云.png")


if __name__ == '__main__':
    itchat.auto_login()
    signature()
