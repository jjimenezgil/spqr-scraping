# Ancient sources data extraction

Repository containing the Scrapy project that performs the data extraction for ClioAI. The scraper executes the extraction of all the greek and roman materials from the [Perseus Collection](https://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman).
Please, for the complete information refer to the ClioAI repository: https://github.com/jjimenezgil/clio-ai

## Data format

The extracted data is loaded into a CSV (which you can find in the dataset folder of the repository). The structure of the CSV is as follows:


## Instructions

- Go to the source folder:
```bash
cd source
```

- Execute the following command in your terminal (remember to change the file name if you want):
```bash
scrapy crawl perseusScraper -O ../dataset/test.csv
````