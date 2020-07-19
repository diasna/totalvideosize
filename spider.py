import scrapy
import math
class TotalVideoSize(scrapy.Spider):
    name = "4anime"
    start_urls = [
        'https://4anime.to/browse?sf_paged=1',
    ]
    total = 0

    def parse(self, response):
        for anime in response.xpath('//div[@id="headerDIV_3"]'):
            yield scrapy.Request(anime.xpath('div/a[@id="headerA_5"]/@href').extract_first(), callback=self.parse_episode)
        next_page_url = response.xpath('//a[@class="nextpostslink"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_episode(self, response):
        for episode in response.xpath('//ul[@class="episodes range active"]/li'):
            episode_link = episode.xpath('a/@href').extract_first()
            yield scrapy.Request(episode_link, callback=self.parse_video_link)

    def parse_video_link(self, response):
        media_url = response.xpath('//source/@src').get()
        yield scrapy.Request(media_url, method="HEAD", callback=self.parse_video_size)

    def parse_video_size(self, response):
        self.total = self.total + int(response.headers['content-length'])
        print(self.convert_size(self.total))

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
