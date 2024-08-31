# Ancient sources data extraction

Repository containing the Scrapy project that performs the data extraction for *ClioAI*. The scraper executes the extraction of all the greek and roman materials from the [Perseus Collection](https://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman).
Please, for the complete information refer to the [ClioAI repository](https://github.com/jjimenezgil/clio-ai).

## Data

The extracted data is loaded into a CSV (which you can find in the dataset folder of the repository). The CSV contains the following fields:
- Author
- Title
- Section
- Text


## Instructions

The best option is to directly download the data that can be found in the dataset folder, since the extraction process could be a long process (several hours, depending on the configuration of the settings.py), and also the ancients authors are not expected to deliver new material, so performing the complete extraction process will not add new data to the current dataset. In any case, you can follow these steps to begin the scraping: 

- Clone the repository and carry out all the process in a local environment (it's a long process, I tried to do it from codespaces but the connection got lost before the process ended).

- Go to the source folder:
```bash
cd source
```

- Execute the following command in your terminal (remember to change the file name if you want):
```bash
scrapy crawl perseusScraper -O ../dataset/test.csv
````