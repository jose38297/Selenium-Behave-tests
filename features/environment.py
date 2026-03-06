from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # mode headless
chrome_options.add_argument("--no-sandbox")  # requis sur CI Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # pour GitHub Actions
chrome_options.add_argument("--disable-gpu")  # parfois nécessaire

driver = webdriver.Chrome(options=chrome_options)

def after_all(context):
    if hasattr(context, "driver"):
        context.driver.quit()




"""
from selenium import webdriver


def before_all(context):

    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

    context.base_url = "https://opensource-demo.orangehrmlive.com"


def after_all(context):

    context.driver.quit()
    
"""