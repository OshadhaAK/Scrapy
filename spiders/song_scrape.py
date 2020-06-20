import sys
sys.path.append(".")
import scrapy
from deranafm.items import DeranafmItem

class Song(scrapy.Spider):
    name = "song_scraper"

    # First Start Url
    start_urls = ["http://www.fmderana.lk/sinhala-music-videos"]

    npages = 2

    # This mimics getting the pages using the next button.
    for i in range(1, npages + 2):
        start_urls.append("http://www.fmderana.lk/sinhala-music-videos/page/" + str(i) + "")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'item col-6 col-sm-4 col-md-3 col-lg-4 col-xl-3')]/article[contains(@class, 'radio-item artist')]/figure/a//@href"):
            # add the scheme, eg http://
            url = "http:" + href.extract()

            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = DeranafmItem()

        # Getting Campaign Title
        item['song'] = response.xpath("//div[contains(@class, 'video-content')]/h1/descendant::text()").extract()[0].strip()

        # Getting Amount Raised
        item['mainArtist'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Main Artist')]/following-sibling::dd[1]/descendant::text()").extract()[0]

        # Goal
        item['music'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Music')]/following-sibling::dd[1]/text()").extract()[0]
        
        # Currency Type (US Dollar Etc)
        item['lyrics'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Lyrics')]/following-sibling::dd[1]/text()").extract()[0]
        
        # Campaign End (Month year etc)
        item['visits'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Visits')]/following-sibling::dd[1]/text()").extract()[0]
        
        # Number of contributors
        item['downloads'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Downloads')]/following-sibling::dd[1]/text()").extract()[0]

        item['videoURI'] = response.xpath("//div[contains(@class, 'video-extra-info')]/dl[contains(@class, 'details-list')]/dt[contains(text(), 'Music')]/following-sibling::dd[1]/text()").extract()[0]

        # Getting Story
        # downloadable_formats_list = response.xpath("//div[contains(@id, 'full-story')]/descendant::text()").extract()
        # downloadable_formats_list = [x.strip() for x in downloadable_formats_list if len(x.strip()) > 0]
        # item['downloadFormats'] = " ".join(downloadable_formats_list)

        # Url (The link to the page)
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        yield item
