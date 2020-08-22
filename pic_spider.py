import re,requests,time,os, json
import config
from urllib.parse import urlencode
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


def get_img_dic(img_id,username, password):#传入图片ID，返回该图片ID下的信息，具体信息见注释
    '''
    img_dic = {
        'illustID' : 插画ID
        'illustTitle' : 插画标题
        'illustDescription' : 插画简介
        'createDate' : 插画创建时间
        'uploadDate' : 插画更新时间
        'tags' : 插画tag,值为列表
        'authorID' : 作者ID
        'authorName' : 作者昵称
        'imgUrl' : 插画原始大小url,值为列表
    }
    '''
    img_dic ={}
    # 登录用户
    session = login(username, password)

    #获取第一个文件的信息，把除了图片url以外的东西先拿到
    url_1 = 'https://www.pixiv.net/ajax/illust/' + img_id
    response_1 = session.get(url_1)
    # 不加以下这些会报错，似乎是因为eval()不能处理布尔型数据
    global false, null, true
    false = 'False'
    null = 'None'
    true = 'True'
    response_1 = eval(response_1.content)['body']
    img_dic['illustID'] = response_1['illustId'] #图片ID
    img_dic['illustTitle'] = response_1['illustTitle'] #图片标题
    taglist = [] #因为有多个tag，所以'tags'的值用列表形式保存
    for tag in response_1['tags']['tags']:
        taglist.append(tag['tag'])
        img_dic['tags'] = ','.join(taglist)
    img_dic['authorID'] = response_1['tags']['tags'][0]['userId']
    img_dic['authorName'] = response_1['tags']['tags'][0]['userName']

    #获取第二个文件的信息，把图片url拿到
    url_2 = 'https://www.pixiv.net/ajax/illust/'+ img_id + '/pages'
    response_2 = session.get(url_2)
    response_2 = eval(response_2.content)['body']
    img_dic['imgUrl'] = []
    for img_url in response_2:
        img_dic['imgUrl'].append(img_url['urls']['original'].replace('\\', ''))
    # print(type(img_dic["tags"]))
    return img_dic

def sentDb(url, pid, username, password):
    img_dic=get_img_dic(pid, username, password)
    data = {
        "url": 'https://www.pixiv.net/artworks/' + img_dic["illustID"],
        "pid": img_dic["illustID"],
        "uid": img_dic["authorID"],
        "title": img_dic["illustTitle"],
        "author": img_dic["authorName"],
        "tag": img_dic["tags"]
    }
    res = requests.post(url=url, data=data)
    # print(res.text)
    return(res.text)

with open("./list.txt", "r") as f:
        strF = f.read()
        if strF:
            datas = json.loads(strF)
            for i in datas:
                sentDb(config.url, str(i), config.username , config.password)
                # print(i)

    
