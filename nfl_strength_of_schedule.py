#!/usr/bin/env python

import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from opponents import scrape_opponents
from standing import scrape_standing


def main():
    print("----- initilizing webdriver -----")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)

    try:
        print("----- scraping opponents data -----")
        opponents = scrape_opponents(driver)
        print("----- scraping standing data -----")
        standing = scrape_standing(driver)
    finally:
        driver.close()

    print("----- calculating strength of schedule -----")

    for i, row in opponents.iterrows():
        wins_sum = 0
        for r in row[1:]:
            wins_sum += int(standing.loc[standing["team_names"] == r, "wins"].values[0])
        standing.loc[standing["team_names"] == row[0], "sos"] = wins_sum/256

    print("----- 2020 NFL strength of schedule list -----")
    print(standing.loc[:, ["city_names", "team_names", "sos"]].sort_values("sos", ignore_index=True))

    file_name = "nfl_strength_of_schedule_2020.csv"
    standing.loc[:, ["city_names", "team_names", "sos"]].sort_values("sos", ignore_index=True).to_csv(file_name, index=False)

if __name__ == '__main__':
    main()
