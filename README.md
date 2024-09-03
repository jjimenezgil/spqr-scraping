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

The best option is to directly download the data that can be found in the dataset folder, since the extraction process could be a long process (several hours, depending on the configuration of the *settings.py*), and also the ancient authors are not expected to deliver new material, so performing the complete extraction process will not add new data to the current dataset. In any case, you can follow these steps to begin the scraping: 

- Clone the repository and carry out all the process in a local environment (it's a long process, I tried to do it from codespaces but the connection got lost before the process ended). Navigate to the directory where you want to clone your repository and execute the following command:
```bash
git clone https://github.com/jjimenezgil/spqr-scraping.git
```

- Make sure *pipenv* is installed. You can install it using *pip*:
```bash
pip install pipenv
```

- Run the following command to install the dependencies specified in the *Pipfile*:
```bash
pipenv install
```

- Activate the virtual environment created by *pipenv*:
```bash
pipenv shell
```

- Go to the source folder:
```bash
cd source
```

- Execute the following command in your terminal (remember to change the file name if you want):
```bash
scrapy crawl perseusScraper -O ../data/ancient_sources.csv
```

- You will see in your terminal the progress of the process. It could take some hours to finish (remember that you can tune the *settings.py* parameters, like CONCURRENT_REQUESTS or DOWNLOAD_DELAY). The CSV file with the data will be generated in the *data* folder.