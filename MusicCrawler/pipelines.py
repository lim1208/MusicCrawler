# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from MusicCrawler import settings
from MusicCrawler.items import SingerItem, AlbumItem, SongItem


class MusicCrawlerPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == SingerItem:
            try:
                self.cursor.execute("SELECT singerId FROM singer WHERE singerId=%s", item['singerId'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute("UPDATE singer SET singerName=%s, picture=%s, albumSize=%s, mvSize=%s "
                                        "WHERE singerId=%s", (item['singerName'], item['picture'], item['albumSize'],
                                                              item['mvSize'], item['singerId']))
                else:
                    self.cursor.execute("INSERT INTO singer (singerId, singerName, picture, albumSize, mvSize) VALUES "
                                        "(%s, %s, %s, %s, %s)", (item['singerId'], item['singerName'], item['picture'],
                                                                 item['albumSize'], item['mvSize']))
                    self.connect.commit()
            except Exception as error:
                print error
            return item

        elif item.__class__ == AlbumItem:
            try:
                self.cursor.execute("SELECT albumId FROM album WHERE albumId=%s", item['albumId'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute("UPDATE album SET singerId=%s, albumName=%s, songCount=%s "
                                        "WHERE albumId=%s", (item['singerId'], item['albumName'],
                                                             item['songCount'], item['albumId']))
                else:
                    self.cursor.execute("INSERT INTO album (albumId, singerId, albumName, songCount) VALUES "
                                        "(%s, %s, %s, %s)", (item['albumId'], item['singerId'],
                                                             item['albumName'], item['songCount']))
                self.connect.commit()
            except Exception as error:
                print error
            return item

        elif item.__class__ == SongItem:
            try:
                self.cursor.execute("SELECT songId FROM song WHERE songId=%s", item['songId'])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute("UPDATE song SET albumId=%s, songName=%s, lyric=%s  "
                                        "WHERE songId=%s", (item['albumId'], item['songName'],
                                                            item['lyric'], item['songId']))
                else:
                    self.cursor.execute("INSERT INTO song (songId, albumId, songName, lyric) VALUES (%s, %s, %s, %s)",
                                        (item['songId'], item['albumId'], item['songName'], item['lyric']))
                self.connect.commit()
            except Exception as error:
                print error
            return item
        else:
            pass
