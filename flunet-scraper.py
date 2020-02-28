from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys
import getopt

types = [
    'Territory',
    'WHO region',
    'Transmission zone',
    'Year',
    'Week',
    'Start date',
    'End date',
    'Collected',
    'Processed',
    'A (H1)',
    'A (H1N1)pdm09',
    'A (H3)',
    'A (H5)',
    'A (not subtyped)',
    'A (total)',
    'B (Yamagata)',
    'B (Victoria)',
    'B (not subtyped)',
    'B (total)',
    'Total positive',
    'Total negative',
    'ILI activity',
]

def process_country(df, driver, wait, output_file, index=0):
    filterBy = Select(driver.find_element_by_id('lstSearchBy'))
    yearFrom = Select(driver.find_element_by_id('ctl_list_YearFrom'))
    weekFrom = Select(driver.find_element_by_id('ctl_list_WeekFrom'))
    yearTo = Select(driver.find_element_by_id('ctl_list_YearTo'))
    weekTo = Select(driver.find_element_by_id('ctl_list_WeekTo'))

    display_button = driver.find_element_by_id('ctl_ViewReport')

    filterBy .deselect_all()

    yearFrom.select_by_value('1995')
    weekFrom.select_by_value('1')
    yearTo.select_by_index(0)
    weekTo.select_by_value("53")
    filterBy.select_by_index(index)
    display_button.click()

    try:
        wait.until(EC.invisibility_of_element((By.ID, 'ctl_ReportViewer_AsyncWait_Wait')))
    except WebDriverException:
        print('Browser closed')
        sys.exit()


    content = driver.page_source
    soup = BeautifulSoup(content, features='lxml')
    try:
        table_rows = soup.find('table', {'cols': '23'}).tbody.contents[3:]
    except:
        print('Failed getting country')
        return df

    for row in table_rows:
        row_values = []
        for j, cell in enumerate(row.findAll('span')):
            row_values.append(cell.text)
        
        df.replace('\\xa0', 'No data')
        df = df.append(pd.DataFrame([row_values], columns=types))

    df.to_csv(output_file, index=None, header=True)
    return df


def scrape_flunet(resume_file, output_file):
    driver = webdriver.Firefox()

    driver.get('https://apps.who.int/flumart/Default?ReportNo=12')
    wait = WebDriverWait(driver, 720)

    filterBy = Select(driver.find_element_by_id('lstSearchBy'))
    region_options = [x.text for x in filterBy.options]

    df = pd.DataFrame(columns=types)
    start = 0

    if resume_file:
        df = pd.read_csv(resume_file)
        start = region_options.index(df['Territory'].iloc[-1]) + 1

    for i in range(start, len(region_options)):
        df = process_country(df, driver, wait, output_file, i)

    driver.close()


def main(argv):
    resume_file = ''
    output_file = ''
    try:
        opts, _ = getopt.getopt(argv, 'hi:o:', ['input=', 'output='])
    except getopt.GetoptError:
        print('flunet-scraper.py -i <input file to resume scraping from> -o <output file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('flunet-scraper.py -i <input file to resume scraping from> -o <output file>')
            sys.exit()
        elif opt in ('-i', '--input'):
            resume_file = arg
        elif opt in ('-o', '--output'):
            output_file = arg
    
    if output_file:
        scrape_flunet(resume_file, output_file)

if __name__ == '__main__':
    main(sys.argv[1:])
