from typing import Iterable

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.db import db
from core.data import WeatherPoint


def scrap(zip: str) -> Iterable[WeatherPoint]:
    # launch url
    url = "https://www.meteoswiss.admin.ch/"

    firefox_options = Options()
    firefox_options.add_argument("-headless")

    # create a new Firefox session
    with webdriver.Firefox(options=firefox_options) as driver:
        driver.implicitly_wait(30)
        driver.get(url)

        # make sure overview tab is selected
        overview_button = driver.find_element_by_id("ui-id-1")
        overview_button.click()

        # select location to get data for
        input_txt = driver.find_element_by_id("forecast_local_input")
        input_txt.send_keys(zip)
        button = driver.find_element_by_class_name("forecast-local__submit")
        button.click()

        while True:
            button = driver.find_element_by_class_name("chart-next")

            bs = BeautifulSoup(driver.page_source, 'lxml')
            table = bs.find("table", {"id": "overview__forecast-table"})

            dataset = pd.read_html(str(table))[0]

            for set in dataset.get_values():
                yield WeatherPoint.create(zip, set[0], set[1], set[2], set[3], set[4])

            if "disabled" in button.get_attribute("class"):
                break

            button.click()


def scrap_and_write(zip: str):
    # todo write an implementation with sqlalchemy.dialecs.postgressql.insert to use the ON CONFLICT clause
    with db.session_scope() as session:
        for wp in scrap(zip):
            session.merge(wp)
