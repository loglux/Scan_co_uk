# Scan.co.uk Scrapy Spider
This repository contains a Scrapy spider designed to scrape product information from Scan.co.uk based on provided search terms and filters.

## Features
- **Search Products on Scan.co.uk**: Directly search for products based on your terms.
- **Filter Results Using Multiple Keywords**: For instance, you can search for "RTX 3080" and filter the results by terms like "Gigabyte, 10GB, OC". The spider supports filtering by multiple comma-separated keywords.
- **Exception Keywords Filter**: Exclude products containing specific keywords from the scraped results. For example, you can exclude products containing the word "refurbished".
- **Out of Stock Suppression**: By default, products that are out of stock are suppressed. An additional key can include them in the results.
- **Save results to a CSV file**.

## Setup and Installation
1. Clone this repository.
```bash
git clone https://github.com/loglux/Scan_co_uk.git
cd Scan_UK/scan_uk
```
2. Setup a virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate 
# On Windows, use: venv\Scripts\activate.bat instead
```
3. Install dependencies.
```bash
pip install scrapy
```
4. Run the spider.
```bash
scrapy crawl scan_search -a search="RTX 3080" -a filter_words="Gigabyte,10GB" -a exception_keywords="Dual" -o output.csv -t csv
```
## Parameters
- **search**: The search term you want to use (e.g., "RTX 3080").
- **filter_words**: Comma-separated list of words to filter search results. Only results containing all of these words will be returned. Use -a filter_mode="any", if you need to change this behaviour. Default is an empty string.
- **filter_mode**: By default, filtering results that contain all specified filter words. However, if you want to change the behavior, set it to "any", which will filter results containing any of the specified filter words.
- **exception_keywords**: Comma-separated list of words that act as negative filters. Results containing any of these words will be excluded. Default is an empty string.
- **include_out_of_stock**: By default, out of stock products are suppressed. If you want to include them, pass include_out_of_stock=True.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
## License
MIT