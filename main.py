import requests
from lxml import etree
import csv

base_url = 'https://www.dytt8.net'
HEADER = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.132 Safari/537.36'
}


def get_detail_url(url):  # 获取进入每部电影的url
    proxy = {
        'http': '120.83.96.22:9999'
    }
    req = requests.get(url, headers=HEADER, proxies=proxy)
    txt = req.text
    html = etree.HTML(txt)
    movies_urls = html.xpath('//ul//b/a/@href')
    # print(movies_urls)
    movies_urls = map(lambda url: base_url + url, movies_urls)
    # print(movies_urls)
    return movies_urls


def get_movies_detail(url):
    movies = {}
    res = requests.get(url,headers=HEADER)
    txt = res.content.decode('gbk')
    html = etree.HTML(txt)
    title = html.xpath("//font[@color='#07519a']/text()")[0]
    movies['片名'] = title
    Zoom = html.xpath("//div[@id='Zoom']")[0]
    imgs = Zoom.xpath(".//img[@border='0']/@src")
    poster = imgs[0]
    movies['海报'] = poster
    infoes = Zoom.xpath('.//text()')

    def get_info(info,str_s):
        return info.replace(str_s,'').strip()

    actors=[]
    for index,info in enumerate(infoes):
        if info.startswith('◎年　　代'):
            info = get_info(info,'◎年　　代')
            movies['年代'] = info
        elif info.startswith('◎产　　地'):
            info = get_info(info,'◎产　　地')
            movies['产地'] = info
        elif info.startswith('◎类　　别'):
            info = get_info(info,'◎类　　别')
            movies['类别'] = info
        elif info.startswith('◎语　　言'):
            info = get_info(info,'◎语　　言')
            movies['语言'] = info
        elif info.startswith('◎字　　幕'):
            info = get_info(info,'◎字　　幕')
            movies['字幕'] = info
        elif info.startswith('◎导　　演'):
            info = get_info(info,'◎导　　演')
            movies['导演'] = info
        elif info.startswith('◎主　　演'):
            info = get_info(info,'◎主　　演')
            actors.append(info)
            for x in range(index+1,len(infoes)):
                actor = infoes[x].strip()
                if actor.startswith('◎简') or actor.startswith('◎标'):
                    break
                actors.append(actor)
            movies['主演']=actors
    download = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movies['迅雷下载地址'] = download
    return movies


def out_info(movies):
    for info in movies:
        if info == '主演':
            k = 0
            for ac in movies[info]:
                if k == 0:
                    print(info + ': ' + ac)
                    k += 1
                else:
                    print('%6s%s' % (' ', ac))
        else:
            print(info + ': ' + movies[info])


def writer_down(movie):
    header = ['片名','海报','年代','产地','类别','语言','字幕','导演','主演','迅雷下载地址']
    with open('movie_GOD.csv','w',encoding='utf-8',newline='') as fp:
        writer = csv.DictWriter(fp,header)
        writer.writeheader()
        writer.writerows(movie)
        print('本次写入完成！')


def spider():
    based_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for i in range(1, 2):
        # movies = []
        movie = []
        url = based_url.format(i)
        # print(url)
        details_urls = get_detail_url(url)
        lis = list(details_urls)
        for movies_url in lis:
            # print(movies_url)
            movies = get_movies_detail(movies_url)
            # get_movies_detail(movies_url)
            # out_info(movies)
            movie.append(movies)#每部电影的信息放进movie里面
    writer_down(movie)
        # for mo in movie:
            # out_info(mo)
            # for split in range(100):
            #     print('-',end='')
            # print('')
        # print(movie)
    print('第'+str(i)+'页')
        #     break
        # break


if __name__ == '__main__':
    url = spider()
