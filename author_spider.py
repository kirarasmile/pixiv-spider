import re,requests,time,os, config, json
from urllib.parse import urlencode
import pic_spider

def login(username, password):  # 登录
    # 模拟一下浏览器
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64503210'
    }

    # 用requests的session模块记录登录的cookie


    session = requests.session()

    #进入登录页获取post_key
    response = session.get('https://accounts.pixiv.net/login?lang=zh')
    post_key = re.findall('<input type="hidden" name="post_key" value=".*?">',
                          response.text)[0]
    post_key = re.findall('value=".*?"', post_key)[0]
    post_key = re.sub('value="', '', post_key)
    post_key = re.sub('"', '', post_key)

    # 将传入的参数用字典的形式表示出来，return_to可以去掉
    data = {
        'pixiv_id': username,
        'password': password,
        'return_to': 'https://www.pixiv.net/',
        'post_key': post_key,
    }

    # 将data post给登录页面，完成登录
    session.post("https://accounts.pixiv.net/login?lang=zh", data=data, headers=head)
    return session


def get_author_img_dic(author_id,username,password):#获取作者的全部作品字典
    #登录用户
    session = login(username, password)
    response = session.get('https://www.pixiv.net/ajax/user/' + author_id +'/profile/all')

    # 不加以下这些会报错，似乎是因为eval()不能处理布尔型数据
    global false, null, true
    false = 'False'
    null = 'None'
    true = 'True'
    author_img_dic = eval(response.content)['body']
    # print(author_img_dic)

    return author_img_dic

def get_author_illusts(author_img_dic): #从author_img_dic中获取作者的插画与动图ID
    author_illusts_dic = author_img_dic['illusts']
    illusts_list = [ key for key,value in author_illusts_dic.items() ]
    print(illusts_list)
    return illusts_list

author_img_dic = get_author_img_dic(config.uid, config.username, config.password)

allList = get_author_illusts(author_img_dic)
fl = open("./list.txt", "w")
fl.write(json.dumps(allList))
fl.close()

