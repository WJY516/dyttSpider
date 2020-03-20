from dyttSpider import dyttSpider


if __name__ == '__main__':
    test_url = 'https://www.dytt8.net/html/gndy/dyzz/index.html'
    spider = dyttSpider()
    spider.get_details(url=test_url)
    for item in spider.li_mvdetail:
        print(item)