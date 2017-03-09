from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import numpy
import random
import time
import csv
import ast
import json
import simplejson

USERNAME = "joe.bloggs@gmail"
PASSWORD = "mumsbirthday"


def login(email, password):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://www.facebook.com/")
    email_elem = driver.find_element_by_id("email")
    email_elem.send_keys(email)
    password_elem = driver.find_element_by_id("pass")
    password_elem.send_keys(password)
    login_elem = driver.find_element_by_id("loginbutton")
    login_elem.click()
    return(driver)

def valid_id(i, driver):
    link = "https://www.facebook.com/%d/about" % int(i)
    driver.get(link)
    try:
        driver.find_element_by_link_text("Go back to the previous page")
    except:
        return(driver, True)
    return(driver, False)

def get_friends_from_element(element):
    friend_ids = []
    for friend_elem in element:
        data_gt = friend_elem.get_attribute('data-gt')
        friend_id = ast.literal_eval(data_gt)
        friend_ids.append(friend_id['engagement']['eng_tid'])
    return(friend_ids)

def friends(i, driver):
    link = "https://www.facebook.com/%d/friends" % int(i)
    driver.get(link)
    total_friends = 0
    friend_limit = 2
    delay = 1 # seconds
    searching = True
    while(True):
        time.sleep(delay)
        friend_elems = driver.find_elements_by_xpath("//div[@class='fsl fwb fcb']/a")
        friend_list = get_friends_from_element(friend_elems)
        if len(friend_elems) == total_friends:
            break
        total_friends = len(friend_list)
        if len(friend_list) == 0:
            print('No friends to show')
            break
        if len(friend_list) >= friend_limit:
            break
        friend_elems[-1].send_keys(Keys.END)
    return(driver, friend_list[0:friend_limit])

def get_friend_tree(i, driver, iterations, connections = set()):
    all_connections = connections
    iter = iterations
    print("-" * iter)
    friend_tree = {'id' : i, 'node_type' : 'leaf', 'friend_ids' : [], 'friends' : {}}
    if iter == 1:
        driver, all_friends = friends(i, driver)
        # unique_friends = [x for x in all_friends if x not in all_connections]
        # cycles_removed = len(all_friends) - len(unique_friends)
        # if cycles_removed > 0:
        #     print(str(cycles_removed) + " cycles removed.")
        # all_connections += unique_friends
        friend_tree['friend_ids'] = all_friends
        if all_friends == []:
            friend_tree['node_type'] = 'marcescent'
        else:
            friend_tree['node_type'] = 'leaf'
        return(friend_tree, all_connections)
    driver, id_is_valid = valid_id(i, driver)
    if id_is_valid == False:
        friend_tree['friend_ids'] = []
        friend_tree['node_type'] = 'invalid'
        return(friend_tree, all_connections)
    else:
        driver, all_friends = friends(i, driver)
        unique_friends = {x for x in all_friends if x not in all_connections}
        cycles_removed = len(all_friends) - len(unique_friends)
        if cycles_removed > 0:
            print(str(cycles_removed) + " cycles removed.")
        all_connections = all_connections | unique_friends
        friend_tree['friend_ids'] = all_friends
        if len(all_friends) == 0:
            friend_tree['node_type'] = 'marcescent'
            return(friend_tree, all_connections)
        else:
            iter -= 1
            branches = {}
            friend_tree['node_type'] = 'stem'
            for j in unique_friends:
                branches[j], all_connections = get_friend_tree(j, driver, iter, all_connections)
            friend_tree['friends'] = branches
            return(friend_tree, all_connections)

def main():
    the_id = '788356078'
    iterations = 3
    driver = login(USERNAME, PASSWORD)
    friend_tree, all_connections = get_friend_tree(the_id, driver, iterations)
    # friend_tree['all_connections'] = all_connections
    
    driver.close()

    output_filename = the_id + '.json'

    with open(output_filename, 'w') as outfile:
        json.dump(friend_tree, outfile)
    
    # with open(the_id, 'w') as outfile:
    #     outfile.write(simplejson.dumps(friend_tree, indent = 4, sort_keys = True))


main()