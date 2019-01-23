# coding: utf-8
import codecs
import sys
import expanddouban
import json
from bs4 import BeautifulSoup

reload(sys)
# 设置python默认编码为utf-8，防止中文写入乱码
sys.setdefaultencoding('utf8')
# 任务1:获取每个地区、每个类型页面的URL
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
# 电影分类list
category_list = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪', '同性',
                 '音乐', '歌舞', '传记', '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠', '情色']
# 地区分类list
location_list = ['中国大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利',
                 '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']
# URL list
url_list = []
# 实现函数构造对应类型和地区的URL地址
def getMovieUrl(category, location):
    url = None
    url_front = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影"
    url_front += ("," + category + "," + location)
    # url_list.append(url_front)
    url = url_front
    return url


# 保存所有URL到output.txt
with open('output.txt', 'w') as f:
    for category in category_list:
        for location in location_list:
            movie_url = getMovieUrl(category, location)
            f.write(movie_url + '\n')
            url_list.append(movie_url)

# 任务2: 获取电影页面 HTML
def getHtml(url):
    html = expanddouban.getHtml(url,True)
    return html

# 任务3: 定义电影类
# 将电影类变量添加进list
class Movie(object):
    """电影类"""
    # 构造函数
    def __init__(self, name, rate, location, category, info_link, cover_link):
        # super(Movie, self).__init__()
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    # 显示类变量
    def displayMovie(self):
           print self.name

name = "肖申克的救赎"
rate = 9.6
location = "美国"
category = "剧情"
info_link = "https://movie.douban.com/subject/1292052/"
cover_link = "https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg"

m = Movie(name, rate, location, category, info_link, cover_link)
# m.displayMovie()
# print(str(m).decode("string_escape"))


# 任务4: 获得豆瓣电影的信息
# 生成电影对象list
"""
return a list of Movie objects with the given category and location.
"""
movies_list=[]
def getMovies(category, location):
    # 取得电影url
    movie_url=getMovieUrl(category,location)
    # 取得url对应电影页html
    page_html=getHtml(movie_url)
    # 取得html内所有电影的name,rate,info_link,cover_link
    soup = BeautifulSoup(page_html, 'html.parser')
    content_div = soup.find(id="app").find(class_="list-wp")

    # 遍历获取直接子元素
    for ele in content_div.find_all("a", recursive=False):
        # 一个电影对应一个字典对象，初始化字典对象
        movie_dic={}
        info_link=ele.get("href")

        if ele.find("p", recursive=False):
            ele_p=ele.find("p", recursive=False)
            name=ele_p.find("span",class_="title").get_text()
            rate=ele_p.find("span",class_="rate").get_text()

        if ele.find(class_="cover-wp"):
            ele_cover=ele.find(class_="cover-wp")
            cover_link=ele_cover.find(class_="pic").find("img").get("src")

        # print(name+rate+location+category+info_link+cover_link)
        movie_dic["name"]=name
        movie_dic["rate"]=rate
        movie_dic["location"]=location
        movie_dic["category"]=category
        movie_dic["info_link"]=info_link
        movie_dic["cover_link"]=cover_link

        movies_list.append(movie_dic)

	# return [name,rate,location,category,info_link,cover_link]
    # print(name+rate+location+category+info_link+cover_link)

getMovies(category_list[0],location_list[0])
# print(movies_list)
# 保存电影list到movies.csv
# with open('movies.csv', 'w') as f:
#     f.write(str(movies_list))

# 保存电影字典到movies.csv
with open('movies.csv', 'w') as f:
    for list_item in movies_list:
        f.write(json.dumps(list_item, encoding="UTF-8", ensure_ascii=False)+'\n')
