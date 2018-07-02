# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class App522Pipeline(object):
    def process_item(self, item, spider):
        return item
'''

from scrapy.utils.project import get_project_settings
import pymysql


class App522Pipeline(object):
    def __init__(self):
        settings=get_project_settings() #获取settings配置，设置需要的信息
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.get('MYSQL_HOST'),
            db=settings.get('MYSQL_DBNAME'),
            user=settings.get('MYSQL_USER'),
            passwd=settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        
    def process_item(self, item, spider):
        try:
            if item['url'].find("/app/") >=0:
                self.cursor.execute(
                    """insert into app(url,appname,downloadcount,size,updated,type,tag,content)
                    value (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (item['url'],item['appname'],item['downloadcount'],item['size'],item['updated'],item['type'],item['tag'],item['content']))
                self.connect.commit()
            else:
                self.cursor.execute("""insert into news (url,title,content) value (%s, %s, %s)""",(item['url'],item['title'],item['content']))
                self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            #log(error)
            print(error)
        return item