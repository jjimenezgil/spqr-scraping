import scrapy


class PerseusSpider(scrapy.Spider):

    # Name of the spider
    name = "perseusScraper"

    # URL list to scrap from 
    start_urls = ["http://www.perseus.tufts.edu/hopper/collection?collection=Perseus:collection:Greco-Roman"]

    def parse(self, response):
        # English texts links
        links = response.xpath('//tr[contains(@class, "trHiddenResults")]/td[contains(., "(English)") and @class="tdAuthor"]/a[@class="aResultsHeader"]')
        yield from response.follow_all(links, self.parse_texts)

        # English texts embedded in lists
        embedded_links = response.xpath('//tr[contains(@class, "trHiddenResults")]/td[contains(., "(English)") and @class="tdAuthor"]/ul/li/a[@class="aResultsHeader"]')
        yield from response.follow_all(embedded_links, self.parse_texts)

    
    def parse_texts(self, response):
        # Get author
        author = response.xpath('//div[@id="header_text"]/h1/text()').get()
        author = author.replace(",", "")

        # Get title
        title = response.xpath('//div[@id="header_text"]/h1/span[@class="title"]/text()').get()

        # Section
        section = response.xpath('//div[@id="main"]/div[@id="content"]/div[@id="navbar_wrapper"]/div[@id="text_navbars"]/div[@class="navbar" and position()=2]/div/a[@class="current odd"]/span/text()').get()

        # Combine text and notes
        text_list = response.xpath('//div[@class="text_container en"]/div[@class="text"]/text()').getall()
        notes_list = response.xpath('//div[@class="text_container en"]/div[@class="footnotes en"]/p/text()').getall()
        
        """
        text = ""
        for i, paragraph in enumerate(text_list):
            if i < len(text_list)-1:
                text = text + paragraph + " (" + notes_list[i] + ") "
            else:
                text = text + paragraph
        """

        return {
            "author": author.strip(),
            "title": title.strip(),
            "section": section.strip(),
            "text": text_list,
            "notes": notes_list
        }