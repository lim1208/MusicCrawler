# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SingerItem(Item):
    """歌手信息"""
    singerId = Field()  # 歌手的ID号，唯一标识
    singerName = Field()  # 歌手的姓名
    picture = Field()  # 歌手的头像
    albumSize = Field()  # 歌手发布的专辑数量
    mvSize = Field()  # 歌手拥有的mv数量


class AlbumItem(Item):
    """专辑信息"""
    singerId = Field()  # 发布专辑的歌手ID号
    albumId = Field()  # 专辑的ID号
    albumName = Field()  # 专辑名称
    songCount = Field()  # 专辑包含的歌曲数量


class SongItem(Item):
    """歌曲信息"""
    albumId = Field()
    songId = Field()  # 歌曲ID号
    songName = Field()  # 歌曲名称
    lyric = Field()  # 歌曲的歌词信息
