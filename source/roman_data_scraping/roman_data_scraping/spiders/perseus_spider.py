import scrapy
import re
from lxml.html import HtmlElement


class PerseusSpider(scrapy.Spider):

    # Name of the spider
    name = "perseusScraper"

    # URL list to scrap from 
    start_urls = ["http://www.perseus.tufts.edu/hopper/collection?collection=Perseus:collection:Greco-Roman"]
        

    def parse(self, response):
        # English texts links
        links = response.xpath('//tr[contains(@class, "trHiddenResults")]/td[contains(., "(English)") and @class="tdAuthor"]/a[@class="aResultsHeader"]')
        yield from response.follow_all(links, self.parse_texts)

        # English texts links embedded in lists
        embedded_links = response.xpath('//tr[contains(@class, "trHiddenResults")]/td[contains(., "(English)") and @class="tdAuthor"]/ul/li/a[@class="aResultsHeader"]')
        yield from response.follow_all(embedded_links, self.parse_texts)

    
    def parse_texts(self, response):
        # Get author
        author = response.xpath('//div[@id="header_text"]/h1/text()').get()
        author = author.replace(",", "")

        # Get title
        title = response.xpath('//div[@id="header_text"]/h1/span[@class="title"]/text()').get()

        # Get section
        num_navbars = int(float(response.xpath('count(//div[@id="main"]/div[@id="content"]/div[@id="navbar_wrapper"]/div[@id="text_navbars"]/div[@class="navbar"])').get()))
        section = ""
        for i in range(num_navbars):
            txt_section = response.xpath('//div[@id="main"]/div[@id="content"]/div[@id="navbar_wrapper"]/div[@id="text_navbars"]/div[@class="navbar" and position()=' + str(i+1) + ']/div/a[@class="current odd"]/span/text()').get()
            if txt_section != None:
                if i == 0:
                    section = txt_section.strip()
                else:
                    section = section + ", " + txt_section.strip()

        # Get main text
        text_list = response.xpath('//div[@class="text_container en"]/div[@class="text"]//text()').getall()
        text = ""
        for i, elem in enumerate(text_list):
            cleaned_text = re.sub(r'[\n\t\"]', ' ', elem)
            cleaned_text = cleaned_text.strip()
            if i == 0:
                text = cleaned_text
            else:
                text = text + " " + cleaned_text
        
        text = re.sub(' +', ' ', text.strip())
        
        # Get notes
        num_notes = int(float(response.xpath('count(//div[@class="text_container en"]/div[@class="footnotes en"]/p)').get()))
        notes_list = []

        if num_notes != None and num_notes > 0:
            for i in range(num_notes):
                note_fragments = response.xpath('//div[@class="text_container en"]/div[@class="footnotes en"]/p[position()=' + str(i + 1) + ']//text()').getall()
                note = ""
                for j, elem in enumerate(note_fragments):
                    cleaned_note = re.sub(r'[\n\t\"]', ' ', elem)
                    cleaned_note = cleaned_note.strip()
                    if j == 0:
                        note = "Note: " + cleaned_note
                    else:
                        note = note + " " + cleaned_note
                
                notes_list.append(note)

        # Get test combination of text and notes
        elements = response.xpath('//div[@class="text_container en"]/div[@class="text"]//node()')
        content = []
        link_count = 1

        for i, elem in enumerate(elements):
            if type(elem.root) == str:
                content.append(elem.get().strip())
            elif elem.root.tag == 'a' and elem.xpath('@id').get() != None and elem.xpath('@id').get().startswith('note-link'):
                content.append('insert_note_' + str(link_count))
                link_count = link_count + 1

        # Return the values that will be saved in CSV
        yield {
            "author": author.strip(),
            "title": title.strip(),
            "section": section,
            "text": text,
            "notes": notes_list,
            "test_content": content
        }

        # Find the "next page" link
        next_page = response.xpath('//div[@id="center_col"]/div[@id="header_nav"]/a[@class="arrow"][img[contains(@alt, "next")]]/@href').get()

        # If a next page exists, follow the link and repeat the process
        if next_page:
            yield response.follow(next_page, callback=self.parse_texts)