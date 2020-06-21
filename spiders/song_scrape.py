import sys
sys.path.append(".")
import scrapy
from items import DeranafmItem

class Song(scrapy.Spider):
    name = "song_scraper"

    start_urls = ["http://www.fmderana.lk/sinhala-music-videos"]

    npages = 66

    # This mimics getting the pages using the next button.
    for i in range(1, npages + 2):
        start_urls.append("http://www.fmderana.lk/sinhala-music-videos/page/" + str(i).strip())

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'item col-6 col-sm-4 col-md-3 col-lg-4 col-xl-3')]/article[contains(@class, 'radio-item artist')]/figure/a[contains(@class, 'inner-click')]//@href"):
            url = "http://www.fmderana.lk/" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        item = DeranafmItem()
        formats = []
        try:
            item['song'] = response.xpath("//div[contains(@class, 'video-content')]/h1/text()").extract()[0].strip()
            item['mainArtist'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Main Artist')]/following-sibling::dd[1]/text()").extract()[0].strip()
            item['music'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Music')]/following-sibling::dd[1]/text()").extract()[0].strip()
            item['lyrics'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Lyrics')]/following-sibling::dd[1]/text()").extract()[0].strip()
            item['visits'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Visits')]/following-sibling::dd[1]/text()").extract()[0].strip()
            item['downloads'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Downloads')]/following-sibling::dd[1]/text()").extract()[0].strip()
            item['videoURI'] = response.xpath("//div[contains(@class, 'embed-responsive embed-responsive-16by9')]/iframe[contains(@class, 'embed-responsive-item')]//@src").extract()[0].strip()
            for j in response.xpath("//div[contains(@class, 'video-icons')]/ul[contains(@class, 'icons-list')]/li/a[contains(@class, 'btn btn-default btn-action btn-download')]//@href").extract():
                formats += [j.strip().split("=")[-1]]
            item['downloadFormats'] = formats
            item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()
        except IndexError:
            pass

        yield item