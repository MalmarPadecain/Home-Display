from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from typing import List

from core import db
from core.data import PhoneCall
import secret


def scrap() -> List[PhoneCall]:
    # launch url
    url = secret.ROUTER_ADDRESS

    firefox_options = Options()
    firefox_options.add_argument("-headless")

    # create a new Firefox session
    with webdriver.Firefox(options=firefox_options) as driver:
        driver.implicitly_wait(30)
        driver.get(url)

        # login
        password_field = driver.find_element_by_id("uiPass")
        password_field.send_keys(secret.ROUTER_PASSWORD)
        driver.find_element_by_id("submitLoginBtn").click()

        # select calls
        driver.find_element_by_id("tel").click()
        driver.find_element_by_id("calls").click()

        # need to find the table through selenium. For some reason bs has trouble parsing the whole page
        table = driver.find_element_by_id("uiCalls")
        table = table.get_attribute('outerHTML')

        # parsing
        soup = BeautifulSoup(table, "lxml")
        table = soup.find(name="table", id="uiCalls")
        for td in soup.find_all("td"):
            if "class" in td.attrs:
                if ("call_out" in td["class"]
                        or "call_in" in td["class"]
                        or "call_in_fail" in td["class"]
                        or "call_rejected" in td["class"]):
                    td.append(td["class"][0])
        dataset = pd.read_html(str(table))[0]

        # crate PhoneCall objects from dataset
        lst = [PhoneCall.create(type, datestr, number) for type, datestr, number, *rest in dataset.values]

        return lst


def scrap_and_write():
    lst = scrap()
    with db.session_scope() as session:
        session.add_all(lst)
