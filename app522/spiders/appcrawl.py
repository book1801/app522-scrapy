# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from app522.items import App522AppItem
from app522.items import App522InfoItem

class AppcrawlSpider(CrawlSpider):
    name = 'appcrawl'
    allowed_domains = ['app522.com']
    start_urls = [
            'https://www.app522.com/app/anzhuo/', #app 安卓
            'https://www.app522.com/app/ios/', #app 苹果
            'https://www.app522.com/app/zh/',#app 综合
            'https://www.app522.com/info/news/'# 资讯
        ]
        
    rules = (
            Rule(LinkExtractor(allow=('/app/anzhuo/')), callback='parse_applist_item'),#/app/anzhuo/
            Rule(LinkExtractor(allow=('/app/ios/')), callback='parse_applist_item'),#/app/ios/
            Rule(LinkExtractor(allow=('/app/zh/')), callback='parse_applist_item'),#/app/zh/
            Rule(LinkExtractor(allow=('/app/anzhuo/(\d+).html$')), callback='parse_applist_item'),#/app/anzhuo/123.html
            Rule(LinkExtractor(allow=('/app/ios/(\d+).html$')), callback='parse_applist_item'),
            Rule(LinkExtractor(allow=('/app/zh/(\d+).html$')), callback='parse_applist_item'),
            Rule(LinkExtractor(allow=('/app/(\d+).html')), callback='parse_app_item'),#/app/123.html
            
            Rule(LinkExtractor(allow=('/info/news/')), callback='parse_newslist_item'),#/info/news/
            Rule(LinkExtractor(allow=('/info/news/(\d+).html')), callback='parse_newslist_item'),#/info/news/123.html
            Rule(LinkExtractor(allow=('/info/(\d+).html')), callback='parse_news_item'),#/info/123.html
        )    
        

    #应用列表页
    def parse_applist_item(self, response):
        #计算cpage的值
        uri=response.url.replace("https://www.app522.com","").replace(".html","")
        p=uri.split("/")[-1]
        cpage=0
        if p=="":
            cpage=1
        else:
            cpage=int(p)
            
        #计算dir
        dir=uri[1]+"/"+uri[2]
        
        if cpage < 2:
            maxpage=response.xpath("//div[@class='pagebar']/span[@class='ptpage']/text()").extract()
            arr=maxpage[0].split("/")
            if len(arr) >1:
                maxpagecode=arr[1]
                maxpagecode=maxpagecode.replace("页","").replace(" ","")
                maxpage_int=int(maxpagecode) + 1
                for page in range(2,maxpage_int):
                    url="https://www.app522.com"+dir+str(page)+".html"
                    yield scrapy.Request(url, callback=self.parse_applist_item)
        
        
        for appurl in response.xpath("//a[@class='app-title']/@href").extract():
            if appurl.find("app522.com") >0:
                yield scrapy.Request(appurl, callback=self.parse_app_item)
            else:
                yield scrapy.Request("https://www.app522.com"+appurl, callback=self.parse_app_item)

    #应用详情页
    def parse_app_item(self,response):
        appname=response.xpath("//h1/text()").extract()[0]
        content=response.xpath("//div[@class='introduce']").extract()[0]
        appinfo_list=response.xpath("//ul[contains(@class,'app-tab')]/li/text()").extract()
        if len(appinfo_list) > 4:
            downloadcount=appinfo_list[0]
            size=appinfo_list[1]
            updated=appinfo_list[2]
            type=appinfo_list[3]
            tag=appinfo_list[4]
            
            appitem=App522AppItem()
            appitem["appname"]=appname
            appitem["downloadcount"]=downloadcount
            appitem["size"]=size
            appitem["updated"]=updated
            appitem["type"]=type
            appitem["tag"]=tag
            appitem["content"]=content
            appitem["url"]=response.url
            
            print("[App]"+response.url)
            
            yield appitem
            
            #print("appname:"+appname)
            #print("downloadcount:"+downloadcount)
            #print("size:"+size)
            #print("updated:"+updated)
            #print("type:"+type)
            #print("tag:"+tag)        
            
    #新闻列表页
    def parse_newslist_item(self,response):
        #计算cpage的值
        uri=response.url.replace("https://www.app522.com","").replace(".html","")
        p=uri.split("/")[-1]
        cpage=0
        if p=="":
            cpage=1
        else:
            cpage=int(p)
        
        if cpage < 2:
            maxpage=response.xpath("//div[@class='pagebar']/span[@class='ptpage']/text()").extract()
            arr=maxpage[0].split("/")
            if len(arr) >1:
                maxpagecode=arr[1]
                maxpagecode=maxpagecode.replace("页","").replace(" ","")
                maxpage_int=int(maxpagecode) + 1
                for page in range(2,maxpage_int):
                    url="https://www.app522.com/info/"+str(page)+".html"
                    yield scrapy.Request(url, callback=self.parse_newslist_item)
            
            
        for infourl in response.xpath("//h3/a[@class='cst-title']/@href").extract():
            if infourl.find("app522.com") > 0:
                yield scrapy.Request(infourl, callback=self.parse_news_item)
            else:
                yield scrapy.Request("https://www.app522.com"+infourl, callback=self.parse_news_item)
    
    #新闻详情页
    def parse_news_item(self,response):
        title=response.xpath("//h2/b/text()").extract()[0]
        content=response.xpath("//div[@class='detail-info']").extract()
        content=content[0]
        del_start=content.find("<div class=\"comment\">")
        content=content[0:del_start]
        
        infoitem=App522InfoItem()
        infoitem["url"]=response.url
        infoitem["title"]=title
        infoitem["content"]=content
        
        print("[News]: "+response.url)
        
        yield infoitem
        