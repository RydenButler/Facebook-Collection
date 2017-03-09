from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import random
import time
import csv

## website where it talks about FB id history
## https://www.quora.com/What-is-the-history-of-Facebooks-user-ID-numbering-system

def login(email, password):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.get("https://www.facebook.com/")
    email_elem = driver.find_element_by_id("email")
    email_elem.send_keys(email)
    password_elem = driver.find_element_by_id("pass")
    password_elem.send_keys(password)
    login_elem = driver.find_element_by_id("loginbutton")
    login_elem.click()
    return driver

def about(driver):
    name_elem = driver.find_element_by_id("fb-timeline-cover-name")
    name = name_elem.text
    about_elem = driver.find_element_by_link_text("Contact and basic info")
    about_elem.click()
    time.sleep(2)
    about_elem = driver.find_element_by_id("pagelet_basic")
    text = (about_elem.text).splitlines()
    try:
        bday = text[text.index("Birthday") + 1]
    except ValueError:
        bday = "NA"
    try:
        gender = text[text.index("Gender") + 1]
    except ValueError:
        gender = "NA"
    try:
        int_in = text[text.index("Interested in") + 1]
    except ValueError:
        int_in = "NA"
    try:
        relig = text[text.index("Religious views") + 1]
    except ValueError:
        relig = "NA"
    try:
        pol = text[text.index("Political views") + 1]
    except ValueError:
        pol = "NA"
    return driver, name, bday, gender, int_in, relig, pol


def location(driver):
    loc_elem = driver.find_element_by_partial_link_text("Places")
    loc_elem.click()
    time.sleep(2)
    loc_elem = driver.find_element_by_id("pagelet_hometown")
    text = (loc_elem.text).splitlines()
    try:
        city = text[text.index("Current city") - 1]
    except ValueError:
        city = "NA"
    try:
        hometown = text[text.index("Home Town") - 1]
    except ValueError:
        hometown = "NA"
    return driver, city, hometown

def marriage(driver):
    mar_elem = driver.find_element_by_link_text("Family and relationships")
    mar_elem.click()
    time.sleep(2)
    mar_elem = driver.find_element_by_id("pagelet_relationships")
    text = (mar_elem.text).splitlines()
    try:
        mar_status = text[text.index("FAMILY MEMBERS") - 1]
    except ValueError:
        mar_status = "NA"
    return driver, mar_status

def valid_id(i, driver):
    link = "https://www.facebook.com/%d/about" % i
    driver.get(link)
    try:
        driver.find_element_by_link_text("Go back to the previous page")
    except:
        return driver, True
    return driver, False


def main():
    random.seed(1)
    found_users = 0
    tries = 1000
    random_ids = []
    random_ids = np.random.randint(low = 100000, high = 999999999, size = tries)
    with open('C:/src/Python/betsy/fb_info2.csv', 'a') as g:
        w = csv.DictWriter(g, fieldnames = ("id", "name", "bday", "gender",
            "int_in", "relig", "pol", "city", "hometown", "mar_status"))
        w.writeheader()
        driver = login("associate.professor.zulio@gmail.com", "1337h4xx0r")
        for i in random_ids[0:tries]:
            driver, is_valid = valid_id(i, driver)
            if(is_valid):
                found_users += 1
                driver, name, bday, gender, int_in, relig, pol = about(driver)
                driver, city, hometown = location(driver)
                driver, mar_status = marriage(driver)
                row = ({"id" : i,
                    "name" : name.encode("utf-8"),
                    "bday" : bday.encode("utf-8"),
                    "gender" : gender.encode("utf-8"),
                    "int_in" : int_in.encode("utf-8"),
                    "relig" : relig.encode("utf-8"),
                    "pol" : pol.encode("utf-8"),
                    "city" : city.encode("utf-8"),
                    "hometown" : hometown.encode("utf-8"),
                    "mar_status" : mar_status.encode("utf-8")})
                w.writerow(row)
    driver.close()
    print("Found " + str(found_users) + " out of " + str(tries) + " tries.")


main()


