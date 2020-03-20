import requests
from lxml import etree


default_headers = {'Host': 'www.dytt8.net',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Connection': 'keep-alive',
                   'Upgrade-Insecure-Requests': '1'}


class dyttSpider:
    def __init__(self, g_headers=default_headers, index_url='https://www.dytt8.net/'):
        self.index_url = index_url
        self.headers = g_headers
        self.se = requests.session()
        self.de_response = ''
        self.dl_response = ''
        self.li_mvdetail = []

    def get_details(self, url):
        self.de_response = self.se.get(url, headers=self.headers)
        if self.de_response.status_code == 200:
            text = self.de_response.content.decode('gbk', 'ignore')
            html = etree.HTML(text)
            li_mv_indexurl = html.xpath('//*[@class="tbspan"]//a/@href')
            for item in li_mv_indexurl:
                mvdetail = {'detail_url': self.index_url + item}
                # TODO 判断是否有重复的
                self.get_download_url(mvdetail['detail_url'], mvdetail)
                self.li_mvdetail.append(mvdetail)
        else:
            pass

    def get_download_url(self, detail_url, detail):
        self.dl_response = self.se.get(detail_url, headers=self.headers)
        if self.dl_response.status_code == 200:
            text = self.dl_response.content.decode('gbk', 'ignore')
            html = etree.HTML(text)
            title = html.xpath('//*[@class="title_all"]/h1/font/text()')
            detail['name'] = title
            download_url = html.xpath('//*[@style="WORD-WRAP: break-word"]//a/@href')
            detail['download_url'] = download_url
        else:
            pass