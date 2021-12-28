import time
from selenium import webdriver
from dotenv import load_dotenv
import os

# get environment variables
load_dotenv()
username = os.environ.get('UPGRAD_EMAIL')
pwd = os.environ.get('UPGRAD_PWD')

# initiate Chrome webdriver using selenium
browser = webdriver.Chrome()
url = 'https://learn.upgrad.com/login'
browser.get(url)


def login_to_upgrad():
    # fill email
    name_email = "email"
    email_input = browser.find_element_by_name(name_email)
    email_input.send_keys(username)

    # fill pwd
    time.sleep(1)
    name_password = "password"
    email_input = browser.find_element_by_name(name_password)
    email_input.send_keys(pwd)

    # click submit
    time.sleep(1)
    submit_btn_class = "submitBtn"
    submit_btn = browser.find_element_by_class_name(submit_btn_class)
    submit_btn.click()

    # pick program
    time.sleep(5)
    path_to_program_heading = "//h2[contains(text(), 'Advanced Certificate Programme in Blockchain Technology - Sept 2021')]"
    program_btn = browser.find_element_by_xpath(path_to_program_heading)
    program_btn.click()


if __name__ == "__main__":
    login_to_upgrad()