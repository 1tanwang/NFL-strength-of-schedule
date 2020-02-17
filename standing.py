#!/usr/bin/env python

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def scrape_standing(driver, year):
    """scrape nfl standing data using webdriver
    and then return a dataframe of processed data"""
    url = "https://www.nfl.com/standings/league/" + year + "/REG"

    try:
        driver.get(url)
        time.sleep(1)

        table = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div/div[2]/div[1]/div/div/div[2]/main/div/div[5]/div/div/div/div/div")

        city_names = table.find_elements_by_class_name("css-7tlc3q")
        team_names = table.find_elements_by_class_name("css-1c42wtk")
        wins = table.find_elements_by_id("overallWin")

        city_names = [c.text for c in city_names]
        team_names = [t.text for t in team_names]
        wins = [int(w.text) for w in wins[1:]]

    except Exception as e:
        print(e)

    df = pd.DataFrame({"city_names": city_names, "team_names": team_names, "wins": wins})

    return df
