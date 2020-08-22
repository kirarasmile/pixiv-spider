# pixiv-spider
## 一个魔改别人的py脚本，主要为setuAPI而服务，通过作者的id爬取相关作品的信息(并非下载图片)
## 感谢原作者
<a href="https://github.com/fandaosi/PIXIV_spider">click here</a>
## setuApi
<a href="https://github.com/kirarasmile/setuAPI">click here</a>
## 食用
* pip install -r  requirements.txt 
* 在config.py中输入你的pixiv账户密码，还有你的setuApi
* python run.py [作者pid]
* 爬取的pid存储在list.txt中
## todo
* 增加代理池，防止因为过多的爬取被ban
## 注意
* 该脚本仅供学习交流，使用后产生的后果(包括但不限于IP被ban)请自己负责