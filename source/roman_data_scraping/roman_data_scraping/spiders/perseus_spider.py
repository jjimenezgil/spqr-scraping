import scrapy
import re
import json


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
        
        # Get notes
        num_notes = int(float(response.xpath('count(//div[@class="text_container en"]/div[@class="footnotes en"]/p)').get()))
        notes_list = []

        if num_notes != None and num_notes > 0:
            for i in range(num_notes):
                note_fragments = response.xpath('//div[@class="text_container en"]/div[@class="footnotes en"]/p[position()=' + str(i + 1) + ']//text()').getall()
                note = ""
                for elem in note_fragments:
                    note = note + " " + elem
                
                cleaned_note = re.sub(r'[\n\t]|\s+', ' ', note.strip())         
                notes_list.append(cleaned_note)

        # Get text
        elements = response.xpath('//div[@class="text_container en"]/div[@class="text"]//node()')
        content = []
        text = ""
        link_count = 1
        note_idx = None

        for i, elem in enumerate(elements):
            if type(elem.root) == str:
                cleaned_text = re.sub(r'[\n\t]|\[\s*\d+\s*\]', ' ', elem.get().strip())
                if note_idx != None and i != note_idx+1 or not cleaned_text.isnumeric(): 
                    content.append(cleaned_text)
            elif elem.root.tag == 'a' and elem.xpath('@id').get() != None and elem.xpath('@id').get().startswith('note-link'):
                content.append('insert_note_' + str(link_count))
                link_count = link_count + 1
                note_idx = i
        
        text = ' '.join(content)
        text = re.sub(' +', ' ', text.strip())

        # Combine text and notes
        for idx, note in enumerate(notes_list):
            # Remove the first word if it's a number
            words = note.split()
            first_word = words[0]
            if(first_word.isnumeric()):
                note = ' '.join(words[1:])

            # Put the note in the correct place
            text_replace = "insert_note_" + str(idx+1)
            text = text.replace(text_replace, "[Note " + str(idx+1) + ": " + note.strip() + "]", 1)

        # Return the values that will be saved in CSV
        yield {
            "author": author.strip(),
            "title": title.strip(),
            "section": section,
            "text": text
        }

        # Find the "next page" link
        next_page = response.xpath('//div[@id="center_col"]/div[@id="header_nav"]/a[@class="arrow"][img[contains(@alt, "next")]]/@href').get()

        # If a next page exists, follow the link and repeat the process
        if next_page:
            yield response.follow(next_page, callback=self.parse_texts)