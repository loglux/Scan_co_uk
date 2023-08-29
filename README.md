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

## Added scan_gpu_spider Functionality

### Features
**Search for GPUs**: The spider now crawls multiple GPU pages to fetch the latest GeForce Graphics Cards details. It covers the RTX 4070 series all the way down to the RTX 3060 series.
**Model Number**: A new feature is added to extract the model number of each GPU.
**Dimensions**: The spider now also extracts the dimensions of the GPU, providing a better understanding of the physical specs.
**Chipset**: The spider can now also fetch the chipset information for each product, to offer more in-depth details about the card.

### How to Run scan_gpu_spider
Navigate to the project directory.
Run 
```bash
scrapy crawl scan_gpu_spider -o output.csv
```
This will start the spider, and the scraped data will be stored in your desired format (e.g., .json, .csv, etc.)

## Required Twisted Version

This project was created and tested with a specific version of the Twisted library to ensure compatibility and proper functioning with the Scrapy spider. The required Twisted version for this project is **Twisted 22.10.0**.

### Scrapy Version and Compatibility

At the time this project was created, the latest available version of Scrapy was **Scrapy 2.10.0**. During development and testing, it was confirmed that this version of Scrapy worked seamlessly with Twisted 22.10.0, providing a stable and reliable environment for scraping.

### Compatibility Issue with Newer Twisted Versions

Since software libraries like Scrapy evolve over time, new versions are released to introduce features, improvements, and bug fixes. However, these updates can sometimes lead to compatibility issues with other libraries that the software relies on.

It has been observed that versions of Twisted newer than 22.10.0, such as **Twisted 28.10.0**, can cause compatibility problems with Scrapy 2.10.0. As a result, it is recommended to maintain the specified Twisted version to ensure that the Scrapy spider works as intended.

### Downgrading Twisted for Compatibility

To mitigate the compatibility issue and ensure a smooth experience, it is advised to downgrade Twisted to the required version. You can achieve this by running the following command:

```bash
pip install --upgrade Twisted==22.10.0
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
## License
MIT