import sys
sys.path.append(".")
import scrapy
from items import SongItem


class Song(scrapy.Spider):
    name = "song_scraper"

    start_urls = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/"]

    npages = 20

    # This mimics getting the pages using the next button.
    for i in range(1, npages + 2):
        start_urls.append("https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(i).strip())

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'col-md-6 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col')]/div[contains(@class, 'pt-cv-ifield')]/h4[contains(@class, 'pt-cv-title')]/a//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)



    def parse_dir_contents(self, response):
        item = SongItem()
        formats = []
        try:
            item['song'] = response.xpath("//div[contains(@class, 'entry-content')]/h2/span/text()").extract()[0].strip()
            item['artist'] = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/div/ul/li/span[contains(text(), 'Artist: ')]/a/text()").extract()[0].strip()
            item['music'] = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/ul/li/span[contains(text(), 'Music: ')]/a/text()").extract()[0].strip()
            lyrics = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/pre/text()").extract()
            for element in lyrics:
                formats.append(element.strip())
            item['lyrics'] = formats
            item['visits'] = response.xpath("//div[contains(@class, 'tptn_counter')]/text()").extract()[0].split(" ")[2].split("V")[0]

            item['writer'] = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/ul/li/span[contains(text(), 'Lyrics: ')]/a/text()").extract()[0].strip()
            item['genre'] = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/div/ul/li/span[contains(text(), 'Genre: ')]/a/text()").extract()
            item['postedBy'] = response.xpath("//div[contains(@class, 'su-column-inner su-u-clearfix su-u-trim')]/div/ul/li/span[contains(text(), 'Posted by: ')]/a/span/text()").extract()[0]
            item['guitarKey'] = response.xpath("//div[contains(@class, 'entry-content')]/h3/text()").extract()[0].split("|")[0].split(":")[1]

        except IndexError:
            pass

        yield item

