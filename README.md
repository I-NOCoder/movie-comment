# douban-movie-commentbox

抓取豆瓣电影最高精彩评论
注：本项目只用于交流技术，请勿用于商业用途。

预览：


### 使用技术

1. 后端： Flask  Mongoengine  Redis  requests  lxml 

2. 前端：React  Mobx  Fetch  Material-UI  ES6  Webpack  Babel

### 开始

#### 虚拟环境和安装应用依赖

```
❯ git clone https://github.com/I-NOCoder/douban-movie-commentbox
❯ virtualenv创建虚拟环境，安装requestments.txt中的依赖。
❯ 修改其中的配置(如Redis，MongoDB)
```

#### 爬虫

1. 已经将豆瓣top250的电影id放到文件中，如果需要其他可自行爬取。
2. 然后启动`python run.py`就开始抓取了。
3. spider/fake_useragent 引用自 https://github.com/dongweiming/fake-useragent

#### 前端开发
1. 已经将编译好的.js文件放在static/js/dist
2. 也可 cd assets npm install 自己编译


开发：

开发时可以先修改server.js里面的主机和端口号，然后启动

目前默认后端使用8100端口，开发模式使用5000端口。


Enjoy it!
