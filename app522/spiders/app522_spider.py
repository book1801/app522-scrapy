import scrapy
from app522.items import App522AppItem
from app522.items import App522InfoItem


'''
class App522Spider(scrapy.Spider):
    name = "app522"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
'''

class App522Spider(scrapy.Spider):
    name="app522"
    list_page_spider_flag={}
    list_page_spider_flag["anzhuo"]=True
    list_page_spider_flag["ios"]=True
    list_page_spider_flag["zh"]=True
    list_page_spider_flag["news"]=True
    
    def start_requests(self):
        urls=[
            'https://www.app522.com/app/anzhuo/', #app 安卓
            'https://www.app522.com/app/ios/', #app 苹果
            'https://www.app522.com/app/zh/',#app 综合
            'https://www.app522.com/info/news/'# 资讯
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    #info 详情页
    def info_parse(self,response):
        title=response.xpath("//h2/b/text()").extract()[0]
        content=response.xpath("//div[@class='detail-info']").extract()
        content=content[0]
        del_start=content.find("<div class=\"comment\">")
        content=content[0:del_start]
        
        infoitem=App522InfoItem()
        infoitem["title"]=title
        infoitem["content"]=content
        
        yield infoitem
        
        
        print("title:"+title)
        print("content:"+content)
        
            
    #app 详情页
    def app_parse(self,response):
        appname=response.xpath("//h1/text()").extract()[0]
        appinfo_list=response.xpath("//ul[contains(@class,'app-tab')]/li/text()").extract()
        if len(appinfo_list) > 4:
            downloadcount=appinfo_list[0]
            size=appinfo_list[1]
            updated=appinfo_list[2]
            type=appinfo_list[3]
            tag=appinfo_list[4]
            #yield MyItem(title=h3)
            
            appitem=App522AppItem()
            appitem["appname"]=appname
            appitem["downloadcount"]=downloadcount
            appitem["size"]=size
            appitem["updated"]=updated
            appitem["type"]=type
            appitem["tag"]=tag
            
            yield appitem
            
            print("appname:"+appname)
            print("downloadcount:"+downloadcount)
            print("size:"+size)
            print("updated:"+updated)
            print("type:"+type)
            print("tag:"+tag)
            
    
    #app 列表页
    def applist_parse(self,response):
        print("applist_parse tag")
        print("app list page:"+response.url)
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
                    yield scrapy.Request(url, callback=self.applist_parse)
        
        
        for appurl in response.xpath("//a[@class='app-title']/@href").extract():
            yield scrapy.Request(appurl, callback=self.app_parse)
        
        print("doing applist_parse dong");    
    
    #info 列表页
    def infolist_parse(self,response):
        print("info list page:"+response.url);
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
                    yield scrapy.Request(url, callback=self.infolist_parse)
            
            
        for infourl in response.xpath("//h3/a[@class='cst-title']/@href").extract():
            yield scrapy.Request(infourl, callback=self.info_parse)
            
    # 页面解析分发器
    def parse(self,response):
        print("current url:"+response.url)
        if response.url.find("/app/anzhuo/") >=0:
            self.applist_parse(response)
        elif response.url.find("/app/ios/") >=0:
            self.applist_parse(response)
            print("go applist ios parse")
        elif response.url.find("/app/zh/") >=0:
            self.applist_parse(response)
            print("go applist zh parse")
        elif response.url.find("/info/news/") >=0:    
            self.infolist_parse(response)
            print("go applist news parse")
        else:
            print("no url go on")
        
        print("parse done!")    
        