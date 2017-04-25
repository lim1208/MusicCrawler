# -*- coding:utf-8 -*-
import json

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from MusicCrawler.items import SingerItem, AlbumItem, SongItem


class NtesMusicSpider(CrawlSpider):
    """爬取网易云音乐数据"""

    host = "http://music.163.com/api/"  # 爬取信息的链接

    name = "ntesmusic"

    start_urls = ['周杰伦']

    crawl_singer = set(start_urls)  # 需要爬取的歌手

    def start_requests(self):
        while self.crawl_singer.__len__():
            singer = self.crawl_singer.pop()  # 取出歌手并从队列中删除
            url_singer = self.host + "search/pc/?s=" + singer + "&limit=1&type=100&offset=0"
            print "开始爬取歌手信息，请求链接为：", url_singer, "。"
            yield Request(url=url_singer, method="POST", callback=self.parse_singer)

    def parse_singer(self, response):
        """爬取歌手信息，包括singerId,singerName,picture,albumsize,mvsize"""
        singer = SingerItem()
        singer_result = json.loads(response.body_as_unicode())
        if singer_result['code'] == 200 and singer_result['result']['artistCount'] == 1:
            artists = singer_result['result']['artists'][0]
            singer['singerId'] = artists['id']
            singer['singerName'] = artists['name']
            singer['picture'] = artists['picUrl']
            singer['albumSize'] = artists['albumSize']
            singer['mvSize'] = artists['mvSize']
            print "歌手信息爬取结束，成功获取该歌手信息。"
        yield singer

        if singer:
            url_album = self.host + "artist/albums/" + str(singer['singerId']) + "?id=" + str(singer['singerId']) + \
                        "&offset=0&total=true&limit=" + str(singer['albumSize'])
            print "开始爬取歌手对应的专辑信息，请求链接为：", url_album, "。"
            yield Request(url=url_album, method="GET", meta={"singerId": singer['singerId']}, callback=self.parse_album)
        else:
            print "该歌手不存在，跳过爬取该歌手相关的所有信息。"

    def parse_album(self, response):
        """开始爬取歌手对应的专辑"""
        album_result = json.loads(response.body_as_unicode())
        if album_result['code'] == 200:
            for hotAlbum in album_result['hotAlbums']:
                album = AlbumItem()
                album['singerId'] = response.meta['singerId']
                album['albumId'] = hotAlbum['id']
                album['albumName'] = hotAlbum['name']
                album['songCount'] = hotAlbum['size']
                yield album
                print "成功爬取歌手ID：", album['singerId'], "的专辑ID为：", album['albumId'], "和专辑名为：", \
                    album['albumName'], ";该专辑总共有歌曲数量：", album['songCount']

                url_song = self.host + "album/" + str(album['albumId']) + "?ext=true&id=" + str(album['albumId']) + \
                           "&offset=0&total=true&limit=" + str(album['songCount'])
                yield Request(url=url_song, method="GET", meta={"albumId": album['albumId']}, callback=self.parse_song)

    def parse_song(self, response):
        song_result = json.loads(response.body_as_unicode())
        if song_result['code'] == 200:
            album_songs = song_result['album']['songs']
            for album_song in album_songs:
                song = SongItem()
                song['albumId'] = response.meta['albumId']
                song['songId'] = album_song['id']
                song['songName'] = album_song['name']
                url_lyric = self.host + "song/lyric?os=pc&id=" + str(song['songId']) + "&lv=-1&kv=-1&tv=-1"
                yield Request(url=url_lyric, method="GET", meta={"song": song}, callback=self.parse_lyric)

    def parse_lyric(self, response):
        song = response.meta['song']
        lyric_result = json.loads(response.body_as_unicode())
        if lyric_result['code'] == 200:
            song['lyric'] = lyric_result['lrc']['lyric']
        yield song
