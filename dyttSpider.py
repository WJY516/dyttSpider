import requests
from lxml import etree


default_headers = {'Host': 'www.dytt8.net',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Connection': 'keep-alive',
                   'Upgrade-Insecure-Requests': '1'}


class DyttSpider:

    def __init__(self, g_headers=default_headers, index_url='https://www.dytt8.net/'):
        self.index_url = index_url
        self.headers = g_headers
        self.se = requests.session()
        self.response = ''
        self.li_mvdetail = []

    def get_html(self, url):
        self.response = self.se.get(url, headers=self.headers)
        if self.response.status_code == 200:
            text = self.response.content.decode('gbk', 'ignore')
            return text
        else:
            return

    def get_details(self, url):
        text = self.get_html(url)
        html = etree.HTML(text)
        li_mv_indexurl = html.xpath('//*[@class="tbspan"]//a/@href')
        for item in li_mv_indexurl:
            mvdetail = {'detail_url': self.index_url + item}
            # TODO 判断是否有重复的
            self.get_download_url(mvdetail['detail_url'], mvdetail)
            self.li_mvdetail.append(mvdetail)

    def get_download_url(self, detail_url, detail):
        text = self.get_html(url=detail_url)
        html = etree.HTML(text)
        title = html.xpath('//*[@class="title_all"]/h1/font/text()')
        detail['name'] = title
        thunder_url = html.xpath('//*[@style="WORD-WRAP: break-word"]//a/@href')
        detail['thunder_url'] = thunder_url
        magnetic_url = html.xpath('//*[@id="Zoom"]//a//@href')
        detail['magnetic_url'] = magnetic_url[0]
