# -*- coding: utf-8 -*-
import scrapy
import json
import io
import sys
import os
import requests
import re
from furl import furl  # 获取url的参数值

# 解决编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# 保存图片的目录
inster_name = 'craziejulia'
pic_dir='D:/爬虫学习/'+inster_name

'''
需要爬取的url
#https://www.instagram.com/craziejulia/?hl=zh-cn
可以看到craziejulia是需要爬取的博主的名字
'''
#94188445_1936411606489510_1621512665806123613_n.jpg
#92906929_220705922585987_799413854828239225_n.jpg
class InstasipderSpider(scrapy.Spider):
    name = 'instasipderj'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables=%7B%22id%22%3A%224003141166%22%2C%22first%22%3A12%7D']
    #start_urls=['https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables=%7B%22id%22%3A%224003141166%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFCMk1Na3dJeFd5NUZ1Y2o2U09QTlFoWXFUb2tPTDlGUkw0RTNDaG40cWp6NkVtY3l0Wk9kWEF3Mmw2Q0UyZUhtQ2xkTzllRm92RVZ3RG1NWkV6elBMYg%3D%3D%22%7D']
    # start_urls=['https://www.instagram.com/graphql/query/?query_hash=9dcf6e1a98bc7f6e92953d5a61027b98&variables=%7B%22id%22%3A%224003141166%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFCWDZLQmpFTGE1eEpaTE1uNml5S1hXLWh6TWM4Nlk4VVhFdTZTelFMeWNKRC1PSFUxU3VWS2NGVkN6VFp5Y25WMklRaC1zak5KSGk3Mm1OeU9qZkhVWA%3D%3D%22%7D']
    def parse(self, response):
        rs = json.loads(response.text.encode())

        display_urls=[]
        nodes = rs.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')

        for i in range(0,len(nodes)):
            # 这边是判断帖子是不是有好几张图，要不然只能爬取到每个帖子的第一张图
            nodes_son = nodes[i].get('node').get('edge_sidecar_to_children')

            if nodes_son == None:
                display_urls.append(nodes[i].get('node').get('display_url'))
            else:
                nodes_son = nodes_son.get('edges')
                for j in range(0,len(nodes_son)):
                    display_urls.append(nodes_son[j].get('node').get('display_url'))
        # print('帖子数：%d'%(i + 1 ))
        self.save_to_loca(display_urls)
        next_cursor = rs.get('data').get('user').get('edge_owner_to_timeline_media')['page_info']['end_cursor']
        if next_cursor is not None:
            '''
            构建下一页的url
            如果是首页不存在after则，去掉末尾的%7D,加上%2C%22after%22%3A%22，再加上next_cursor,如果后面
            有== 去掉，再加上%3D%3D%22%7D

            如果不是首页，则更新%2C%22after%22%3A%22和%3D%3D%22%7D中的next_cursor(去掉 ==)
            这段代码解决了ins动态加载的问题
            '''
            f = str(furl(response.url))

            if next_cursor.endswith('=='):
                next_cursor = next_cursor.replace('==','')
            if 'after' not in f:
                f =f[:-3]+'%2C%22after%22%3A%22'+next_cursor+'%3D%3D%22%7D'
            else:
                f =re.sub(r'%2C%22after%22%3A%22(.*)%3D%3D%22%7D','%2C%22after%22%3A%22'+next_cursor+'%3D%3D%22%7D',f)
            yield scrapy.Request(url=f, callback=self.parse,dont_filter=True)

    def save_to_loca(*display_urls):

        for i in range(0, len(display_urls[1])):

            # 保存图片的路径
            # https://scontent-nrt1-1.cdninstagram.com/v/t51.2885-15/e35/94188445_1936411606489510_1621512665806123613_n.jpg?_nc_ht=scontent-nrt1-1.cdninstagram.com&_nc_cat=110&_nc_ohc=30ziKGTCszsAX-72TfD&oh=9d99688290637b771d8267ffe08e9b72&oe=5ED103AF
            pic_name = display_urls[1][i].split('?')[0].split('/')[-1]
            path = pic_dir + '/' +pic_name
            # print(path)
            # 保存图片到指定路径
            try:
                if not os.path.exists(pic_dir):
                    os.mkdir(pic_dir)
                if not os.path.exists(path):
                    pic_url = requests.get(display_urls[1][i])
                    with open(path,'wb') as f:
                        f.write(pic_url.content)
                        f.close()
                        print('文件保存成功')
                else:
                    print('文件已经存在')
            except Exception as e:
                print(e)
'''
处理动态加载next page的问题：

page_info->has_next_page：flase:没有下一页（或者end_cursor=null）

还要处理下视频和图片的问题
'''


