#!/usr/bin/env python

import time
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_opponents(driver, year):
    """scrape the opponents set data using webdriver
    and then return a dataframe of processed data"""
    try:
        url = "http://www.nfl.com/news/story/0ap3000001093515/article/opponents-for-each-team-set-for-2020-nfl-season"
        driver.get(url)
        time.sleep(1)

        article = driver.find_element_by_class_name("articleText")
        sections = article.text.split("\n")
    except Exception as e:
        print(e)

    data = _process_webdata(sections[3:])
    df = pd.DataFrame(data)

    return df


def _process_webdata(content):
    """process the input webpage data and save to dataframe"""
    home_header = re.compile("^Home")
    away_header = re.compile("^Away")

    opponents = []
    temp_list = []
    for line in content:
        if home_header.match(line) is not None:
            temp_list += line[6:].replace(".", "").split(", ")
        elif away_header.match(line) is not None:
            temp_list += line[6:].replace(".", "").split(", ")
            temp_list = [t.split(" ")[-1] for t in temp_list]
            opponents.append(temp_list)
        else:
            temp_list = []
            temp_list.append(line)

    return opponents
