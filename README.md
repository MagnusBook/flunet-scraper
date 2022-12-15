# FluNet-Scraper

This project scrapes the [FluNet](https://apps.who.int/flumart/Default?ReportNo=12) website for influenza data. The resulting data from all the countries is saved in `data/global_influenza.csv`.

**NOTE:** WHO have made the raw CSV files available through this link [https://www.who.int/teams/global-influenza-programme/surveillance-and-monitoring/influenza-surveillance-outputs](https://www.who.int/teams/global-influenza-programme/surveillance-and-monitoring/influenza-surveillance-outputs). That would be a better and more up-to-date version of the data scraped here.

## Requirements

Requirements are contained within `requirements.txt`, and can be installed using `pip install --requirement requrirements.txt`. This project uses FireFox for the web driver, and requires the [geckodriver](https://github.com/mozilla/geckodriver/releases) to be in the path. This can be changed to other browsers/drivers if needed.


## Usage
This script allows for an input file to be passed as an argument in case the execution failed at some point. If an input file is passed, the script will continue from the last country in the file.

```
python flunet-scraper.py -i <input file to resume scrping from> -o <output file>
```
