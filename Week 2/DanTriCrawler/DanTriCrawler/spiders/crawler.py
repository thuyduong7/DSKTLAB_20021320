import scrapy
from DanTriCrawler.items import PaperCrawler


class DanTri(scrapy.Spider):
    name = "dantri"
    path_dt = 'https://dantri.com.vn'
    start_urls = [
        'https://dantri.com.vn/nhip-song-tre/gioi-tre-lam-van-phong-that-lung-buoc-bung-tiet-kiem-cho-tuong-lai'
        '-20211129080933738.htm', ]
    index = 1

    def parse(self, response):
        paper = PaperCrawler()
        paper['index'] = self.index
        paper['title'] = response.css('h1.dt-news__title::text').get().strip()
        paper['link'] = response.css('link[rel="canonical"]::attr(href)').get()
        paper['date'] = response.css('span.dt-news__time::text').get()
        paper['intro'] = response.css('div.dt-news__sapo h2::text').get()
        paper['body'] = response.css('div.dt-news__content p::text').getall()
        if self.index > 10000:
            return
        self.index += 1
        yield paper
        next_links = self.get_next_links(response)
        if next_links is not None:
            for link in next_links:
                yield scrapy.Request(link, callback=self.parse)

    def get_next_links(self, response):
        links = response.css('h3.news-item__title a::attr(href)').getall()
        qualified_links = []
        for link in links:
            if self.path_dt + link not in self.start_urls:
                self.start_urls.append(self.path_dt + link)
                qualified_links.append(self.path_dt + link)
        if qualified_links is not None:
            return qualified_links
        return None
