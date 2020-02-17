#!/usr/bin/env python

import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from opponents import scrape_opponents
from standing import scrape_standing


def main():
    year = "2020"
    sos = "sos_" + year

    print("----- initilizing webdriver -----")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)

    try:
        print("----- scraping opponents data -----")
        opponents = scrape_opponents(driver, year)
        print("----- scraping standing data -----")
        standing = scrape_standing(driver, year)
    finally:
        driver.close()
        driver.quit()

    print("----- calculating strength of schedule -----")

    for i, row in opponents.iterrows():
        wins_sum = 0
        for r in row[1:]:
            wins_sum += int(standing.loc[standing["team_names"] == r, "wins"].values[0])
        standing.loc[standing["team_names"] == row[0], sos] = wins_sum/256

    df_sos = standing.loc[:, ["city_names", "team_names", sos]].sort_values(sos, ignore_index=True)
    df_sos["Team"] = df_sos["city_names"] + " " + df_sos["team_names"]
    df_sos["rank_"+year] = df_sos.index + 1
    df_sos[sos] = df_sos[sos].round(3)
    df_sos = df_sos[["Team", sos, "rank_"+year]]

    print("----- 2020 NFL strength of schedule list -----")
    print(df_sos)

    file_name = "nfl_strength_of_schedule.csv"
    try:
        df_prev = pd.read_csv(file_name)
        df_sos = df_sos.merge(df_prev, left_on="Team", right_on="Team")
        df_sos.to_csv(file_name, index=False, float_format="%.3f")
    except pd.errors.EmptyDataError:
        df_sos.to_csv(file_name, index=False, float_format="%.3f")
    except FileNotFoundError:
        df_sos.to_csv(file_name, index=False, float_format="%.3f")

if __name__ == '__main__':
    main()
