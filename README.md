# FluNet-Scraper

This project scrapes the [FluNet](https://apps.who.int/flumart/Default?ReportNo=12) website for influenza data. The resulting data from all the countries is saved in `data/global_influenza.csv`.

## Requirements

Requirements are contained within `requirements.txt`, and can be installed using `pip install --requirement requrirements.txt`. This project uses FireFox for the web driver, and requires the [geckodriver](https://github.com/mozilla/geckodriver/releases) to be in the path. This can be changed to other browsers/drivers if needed.

