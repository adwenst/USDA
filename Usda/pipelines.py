# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor


class PlantPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        mysql_params = dict(
            mysql_host=settings.get('MYSQL_HOST'),
            mysql_port=settings.get('MYSQL_PORT'),
            mysql_user=settings.get('MYSQL_USER'),
            mysql_passwd=settings.get('MYSQL_PASSWD'),
            mysql_dbname=settings.get('MYSQL_DBNAME'),
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **mysql_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 在此处将数据存储到数据库中，所有的数据都会经过这一函数
        # 数据是可以通过dict(item)转化为字典形式，可以打印观察数据形式
        # 所有的字典中都有Symbol这一项，这是主键，其他的部分字段
        # 数据库中表可能没有，需要在数据库中动态修改表
        return item
