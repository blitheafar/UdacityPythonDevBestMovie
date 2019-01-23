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
    html = expanddouban.getHtml(url, True)
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
movies_list = []
def getMovies(category, location):
    # 取得电影url
    movie_url = getMovieUrl(category, location)
    # 取得url对应电影页html
    page_html = getHtml(movie_url)
    # 取得html内所有电影的name,rate,info_link,cover_link
    soup = BeautifulSoup(page_html, 'html.parser')
    content_div = soup.find(id="app").find(class_="list-wp")

    # 遍历获取直接子元素
    for ele in content_div.find_all("a", recursive=False):
        info_link = ele.get("href")

        if ele.find("p", recursive=False):
            ele_p = ele.find("p", recursive=False)
            name = ele_p.find("span", class_="title").get_text()
            rate = ele_p.find("span", class_="rate").get_text()

        if ele.find(class_="cover-wp"):
            ele_cover = ele.find(class_="cover-wp")
            cover_link = ele_cover.find(class_="pic").find("img").get("src")

        movies_list.append('{},{},{},{},{},{}'.format(name,rate,location,category,info_link,cover_link))

# 生成一组list包含电影对象
# 任务5: 构造电影信息数据表,
"""
从网页上选取你最爱的三个电影类型，然后获取每个地区的电影信息后，
我们可以获得一个包含三个类型、所有地区，评分超过9分的完整电影对象的列表。
将列表输出到文件 movies.csv
"""
# 最喜欢的3类电影对象保存在movies_list中
favorite_category_list=["剧情","喜剧","动画"]
for category_item in favorite_category_list:
    for location_item in location_list:
        getMovies(category_item,location_item)

# 遍历movies_list，保存电影字典到movies.csv
with open('movies.csv', 'w') as f:
    for list_item in movies_list:
        f.write(json.dumps(list_item, encoding="UTF-8", ensure_ascii=False)[1:-1] + '\n')

# 任务6: 统计电影数据,结果输出文件到output.txt
"""
统计你所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少？
你可能需要自己把这个任务拆分成多个步骤，统计每个类别的电影个数，统计每个类别每个地区的电影个数，排序找到最大值
"""
